# Feature Trace Standard

The canonical format is long CSV:

`timestamp,bar_index,feature_id,feature_type,stage,column_name,value,value_type,source_oracle`

Supported stages are `data`, `indicator`, `signal`, `transform`, `gate`, `decision`, `execution`, `sizing`, `guard`, `alert`, and `visualization`.

Wide traces are allowed for adapters, but must be normalized before comparison:

`timestamp,bar_index,feature_id,<feature-specific columns...>`

Default tolerance is `numeric_abs_tol=1e-8`, `numeric_rel_tol=1e-6`, with configurable tick tolerance for price-like columns. Booleans and reason codes are exact match.
