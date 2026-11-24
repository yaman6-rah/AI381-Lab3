import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri("http://localhost:5000")
c = MlflowClient()
exp = c.get_experiment_by_name("churn")
runs = c.search_runs([exp.experiment_id], order_by=["attributes.start_time ASC"])
print(f"experiment={exp.name} id={exp.experiment_id} runs={len(runs)}\n")
need_params = {"model", "data_file", "data_sha256"}
need_metrics = {"auc", "f1", "p95_latency_ms", "size_kb"}
for r in runs:
    p, m, t = r.data.params, r.data.metrics, r.data.tags
    print(f"## {t['mlflow.runName']}  run_id={r.info.run_id}  status={r.info.status}")
    print("  tags     :", {k: t[k] for k in ("batch", "git_sha", "model_uri")})
    print(
        "  params   :",
        {
            k: p[k]
            for k in sorted(p)
            if k in need_params
            or k in ("clf__max_iter", "clf__n_estimators", "clf__max_depth", "clf__learning_rate", "clf__random_state")
        },
    )
    print(f"  n_params : {len(p)}")
    print("  metrics  :", m)
    slices = [k for k in m if k.startswith("f1_contract_")]
    ok = need_params <= p.keys() and need_metrics <= m.keys() and len(slices) == 3
    arts = [a.path for a in c.list_artifacts(r.info.run_id, "model")]
    print("  artifacts:", arts)
    mlmodel = [a for a in arts if a.endswith("MLmodel")]
    print(f"  CHECK params+metrics+3 slices: {ok}; MLmodel present: {bool(mlmodel)}")
    local = mlflow.artifacts.download_artifacts(run_id=r.info.run_id, artifact_path="model/MLmodel")
    txt = open(local).read()
    sig = txt.split("signature:")[1].split("\n  type:")[0] if "signature:" in txt else "MISSING"
    print("  signature (head):", sig.strip()[:230].replace("\n", " "))
    print("  input_example   :", any("input_example" in a for a in arts))
    print()
