# [Change the runtime interface › Which runtime interface fits the required operation?]   19 visits, 7 experts

options: Use a supported execution backend (7) | Use the native training API (1) | Use the estimator wrapper (1)

check first: E62 The configured accelerator or dataframe backend does not support a required operation.  imp 0.90 → +Use a supported execution backend  [first in 17/19 visits that checked it]
then:        E64 The estimator wrapper already supports the required stopping and probability outputs.  imp 0.70 → +Use the estimator wrapper  [first in 1/2 visits that checked it]
then:        E63 The current wrapper cannot expose the needed custom metric or iteration control.  imp 0.75 → +Use the native training API  [first in 1/2 visits that checked it]
enough when:  top option >= 87% (lower quartile over 19 visits) or >= 81 points ahead; median 1 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 100% of visits