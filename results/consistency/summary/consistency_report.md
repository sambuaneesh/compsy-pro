# Output-Level Counterfactual Consistency Summary

This report evaluates whether a causal language model assigns higher forced-choice likelihood to `yes` for identical sentence controls and to `no` for counterfactual role-reversal or negation pairs. The experiment is a dataset-only behavioral diagnostic, not a human-alignment experiment.

## Accuracy and Bias

| Model | Phenomenon | Condition | n | Accuracy | Yes-rate | Mean yes-minus-no margin |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| gpt2 | negation | counterfactual | 1500 | 0.9380 | 0.0620 | -0.4468 |
| gpt2 | negation | identity_control | 1500 | 0.2187 | 0.2187 | -0.2346 |
| gpt2 | role_reversal | counterfactual | 1500 | 0.9760 | 0.0240 | -0.5579 |
| gpt2 | role_reversal | identity_control | 1500 | 0.0393 | 0.0393 | -0.4427 |

## CSS Shift Versus Output Discrimination

For counterfactual rows, `no_margin = score(no) - score(yes)`. Positive correlations mean larger representation shifts are associated with stronger output-level rejection of the counterfactual as meaning-preserving.

| Output model | Metric model | Phenomenon | Metric | n | Spearman r | p |
| --- | --- | --- | --- | ---: | ---: | ---: |
| gpt2 | bert-base-uncased | negation | delta_cos | 1500 | -0.0359 | 0.165 |
| gpt2 | bert-base-uncased | negation | delta_frob | 1500 | -0.0042 | 0.872 |
| gpt2 | bert-base-uncased | negation | delta_l2 | 1500 | -0.0253 | 0.328 |
| gpt2 | bert-base-uncased | negation | delta_token_aligned | 1500 | -0.1277 | 7.02e-07 |
| gpt2 | bert-base-uncased | role_reversal | delta_cos | 1500 | 0.0444 | 0.0854 |
| gpt2 | bert-base-uncased | role_reversal | delta_frob | 1500 | 0.0233 | 0.366 |
| gpt2 | bert-base-uncased | role_reversal | delta_l2 | 1500 | 0.0554 | 0.032 |
| gpt2 | bert-base-uncased | role_reversal | delta_token_aligned | 1500 | 0.0786 | 0.00232 |
| gpt2 | gpt2 | negation | delta_cos | 1500 | 0.1592 | 5.68e-10 |
| gpt2 | gpt2 | negation | delta_frob | 1500 | 0.1257 | 1.04e-06 |
| gpt2 | gpt2 | negation | delta_l2 | 1500 | 0.0932 | 0.0003 |
| gpt2 | gpt2 | negation | delta_token_aligned | 1500 | -0.1671 | 7.36e-11 |
| gpt2 | gpt2 | role_reversal | delta_cos | 1500 | 0.0322 | 0.213 |
| gpt2 | gpt2 | role_reversal | delta_frob | 1500 | -0.0081 | 0.754 |
| gpt2 | gpt2 | role_reversal | delta_l2 | 1500 | 0.0183 | 0.479 |
| gpt2 | gpt2 | role_reversal | delta_token_aligned | 1500 | -0.0209 | 0.418 |
| gpt2 | roberta-base | negation | delta_cos | 1500 | 0.1266 | 8.77e-07 |
| gpt2 | roberta-base | negation | delta_frob | 1500 | 0.1359 | 1.26e-07 |
| gpt2 | roberta-base | negation | delta_l2 | 1500 | 0.0678 | 0.00865 |
| gpt2 | roberta-base | negation | delta_token_aligned | 1500 | -0.0676 | 0.00878 |
| gpt2 | roberta-base | role_reversal | delta_cos | 1500 | -0.0060 | 0.815 |
| gpt2 | roberta-base | role_reversal | delta_frob | 1500 | -0.0168 | 0.516 |
| gpt2 | roberta-base | role_reversal | delta_l2 | 1500 | -0.0002 | 0.992 |
| gpt2 | roberta-base | role_reversal | delta_token_aligned | 1500 | 0.0754 | 0.00348 |
