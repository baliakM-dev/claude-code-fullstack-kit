# Grafana / Prometheus / Loki / Tempo observability

Use when adding or reviewing the local or deployed observability stack. Start from operational questions, not from the desire to run more containers.

## Responsibilities
- Prometheus: numeric time-series metrics and alert inputs.
- Loki: logs; labels identify low-cardinality streams, not individual users/requests.
- Tempo: distributed traces.
- Grafana: visualization/correlation across the configured data sources.
- OpenTelemetry Collector or Grafana Alloy: preferred collection/processing boundary when batching, retry, enrichment or backend decoupling is required. Direct export can remain acceptable for a small local demo when explicitly documented.

Do not run Elasticsearch/Kibana merely to duplicate Loki unless the project has a separate search/analytics requirement.

## Metrics
- For request-serving services prioritize traffic, errors, latency and saturation/resource signals.
- Use bounded labels. Never put user ID, email, trace ID, random UUID or other unbounded values into Prometheus labels.
- Prefer base units and stable names. Do not generate metric names from runtime values.
- Keep Actuator/metrics endpoints private or protected; monitoring endpoints are not public product APIs.
- Alerts require an actionable condition and owner/runbook; a dashboard panel is not automatically an alert.

## Logs
- Prefer structured application logs with timestamp, level, service/environment, logger/event, trace/span correlation where available.
- Redact credentials, tokens, cookies and unnecessary personal/financial data before collection.
- Loki labels must remain low-cardinality and long-lived (for example service/environment). Do not use trace ID, request ID, user ID, order/payment ID or arbitrary URL as a Loki label; keep such values in log content or structured metadata.
- Configure retention and storage deliberately. Infinite retention is not a default requirement.

## Traces
- Use OpenTelemetry semantic conventions where supported.
- Add custom spans only around meaningful operations not already covered by instrumentation; avoid tracing every trivial method.
- Do not attach secrets, full request/response bodies or high-volume personal data to span attributes.
- Sampling is an explicit operational decision. Local development may use full sampling; production settings must be justified by traffic, cost and troubleshooting needs.
- Correlate traces with logs/metrics when practical, but do not duplicate whole log records as span attributes.

## Docker topology and persistence
- Keep Grafana, Prometheus, Loki, Tempo and collector endpoints private by default. Expose Grafana through the chosen ingress/auth boundary; do not publicly expose raw admin/query endpoints without a requirement.
- Give stateful components persistent storage only where the selected mode requires it, and document what is disposable in local development versus backed up in production.
- Pin/configure compatible versions and validate configuration with the component's own tooling or startup checks.
- Health checks should distinguish collector/backend unavailability from application health; observability failure must not normally make the business API unavailable unless explicitly required.

## Evidence for a portfolio project
Demonstrate at least one end-to-end incident path, for example:
1. generate a controlled failing/slow request;
2. observe the metric/latency in Grafana;
3. locate the correlated structured log;
4. open the matching trace and identify the slow/failing span;
5. explain what would alert and what remains intentionally unmonitored.

A screenshot alone is weaker evidence than repeatable configuration plus a documented reproduction.

References:
- Prometheus instrumentation: https://prometheus.io/docs/practices/instrumentation/
- Prometheus naming/cardinality: https://prometheus.io/docs/practices/naming/
- Loki label guidance: https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/
- Tempo tracing guidance: https://grafana.com/docs/tempo/latest/set-up-for-tracing/instrument-send/best-practices/
