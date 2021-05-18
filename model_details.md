## Model Details

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4739146.svg)](https://doi.org/10.5281/zenodo.4739146)

Please use the above DOI if you wish to cite this model.

The model is available on the [huggingface model hub](https://huggingface.co/rti-international/distilroberta-ncrp-classification) for use with the `transformers` library. 

It is also available as a [GitHub repository](https://github.com/RTIInternational/distilroberta-ncrp-classification). The repository contains the model converted to the ONNX format on the [releases page](https://github.com/RTIInternational/distilroberta-ncrp-classification/releases). This application uses the quantized ONNX version of the model to make inferences.

### Cross-Validation Performance

#### Overall Metrics

| Metric   | Value |
| -------- | ----- |
| Accuracy | 0.932 |
| MCC      | 0.93  |

 

| Metric    | precision | recall | f1-score |
| --------- | --------- | ------ | -------- |
| macro avg | 0.81      | 0.785  | 0.793    |

*Note*: These are the average of the values *per fold*, so *macro avg* is the average of the macro average of all categories per fold.

#### Per-Category Metrics

| Category                                               | precision | recall | f1-score | support |
| ------------------------------------------------------ | --------- | ------ | -------- | ------- |
| AGGRAVATED ASSAULT                                     | 0.952     | 0.955  | 0.953    | 4085    |
| ARMED ROBBERY                                          | 0.959     | 0.954  | 0.956    | 1021    |
| ARSON                                                  | 0.952     | 0.955  | 0.953    | 344     |
| ASSAULTING PUBLIC OFFICER                              | 0.913     | 0.913  | 0.913    | 588     |
| AUTO THEFT                                             | 0.961     | 0.962  | 0.961    | 1660    |
| BLACKMAIL/EXTORTION/INTIMIDATION                       | 0.874     | 0.845  | 0.859    | 652     |
| BRIBERY AND CONFLICT OF INTEREST                       | 0.792     | 0.807  | 0.799    | 216     |
| BURGLARY                                               | 0.98      | 0.98   | 0.98     | 2214    |
| CHILD ABUSE                                            | 0.804     | 0.785  | 0.793    | 139     |
| COCAINE OR CRACK VIOLATION OFFENSE UNSPECIFIED         | 0.794     | 0.837  | 0.814    | 47      |
| COMMERCIALIZED VICE                                    | 0.821     | 0.787  | 0.803    | 666     |
| CONTEMPT OF COURT                                      | 0.979     | 0.985  | 0.982    | 2946    |
| CONTRIBUTING TO DELINQUENCY OF A MINOR                 | 0.523     | 0.386  | 0.43     | 50      |
| CONTROLLED SUBSTANCE - OFFENSE UNSPECIFIED             | 0.867     | 0.791  | 0.826    | 280     |
| COUNTERFEITING (FEDERAL ONLY)                          | 0         | 0      | 0        | 2       |
| DESTRUCTION OF PROPERTY                                | 0.972     | 0.969  | 0.97     | 2560    |
| DRIVING UNDER INFLUENCE - DRUGS                        | 0.568     | 0.608  | 0.586    | 34      |
| DRIVING UNDER THE INFLUENCE                            | 0.95      | 0.95   | 0.95     | 2195    |
| DRIVING WHILE INTOXICATED                              | 0.989     | 0.98   | 0.984    | 2391    |
| DRUG OFFENSES - VIOLATION/DRUG UNSPECIFIED             | 0.91      | 0.906  | 0.908    | 3113    |
| DRUNKENNESS/VAGRANCY/DISORDERLY CONDUCT                | 0.873     | 0.854  | 0.863    | 380     |
| EMBEZZLEMENT                                           | 0.789     | 0.715  | 0.748    | 100     |
| EMBEZZLEMENT (FEDERAL ONLY)                            | 0         | 0      | 0        | 1       |
| ESCAPE FROM CUSTODY                                    | 0.988     | 0.991  | 0.989    | 4035    |
| FAMILY RELATED OFFENSES                                | 0.736     | 0.776  | 0.755    | 442     |
| FELONY - UNSPECIFIED                                   | 0.669     | 0.723  | 0.691    | 122     |
| FLIGHT TO AVOID PROSECUTION                            | 0.546     | 0.424  | 0.476    | 38      |
| FORCIBLE SODOMY                                        | 0.806     | 0.807  | 0.805    | 76      |
| FORGERY (FEDERAL ONLY)                                 | 0         | 0      | 0        | 2       |
| FORGERY/FRAUD                                          | 0.911     | 0.926  | 0.918    | 4687    |
| FRAUD (FEDERAL ONLY)                                   | 0         | 0      | 0        | 2       |
| GRAND LARCENY - THEFT OVER $200                        | 0.955     | 0.969  | 0.962    | 2412    |
| HABITUAL OFFENDER                                      | 0.75      | 0.645  | 0.689    | 53      |
| HEROIN VIOLATION - OFFENSE UNSPECIFIED                 | 0.868     | 0.824  | 0.843    | 24      |
| HIT AND RUN DRIVING                                    | 0.923     | 0.935  | 0.929    | 303     |
| HIT/RUN DRIVING - PROPERTY DAMAGE                      | 0.941     | 0.922  | 0.931    | 362     |
| IMMIGRATION VIOLATIONS                                 | 0.867     | 0.678  | 0.759    | 19      |
| INVASION OF PRIVACY                                    | 0.922     | 0.927  | 0.924    | 1235    |
| JUVENILE OFFENSES                                      | 0.912     | 0.862  | 0.885    | 144     |
| KIDNAPPING                                             | 0.942     | 0.926  | 0.933    | 553     |
| LARCENY/THEFT - VALUE UNKNOWN                          | 0.939     | 0.942  | 0.941    | 3139    |
| LEWD ACT WITH CHILDREN                                 | 0.789     | 0.836  | 0.811    | 596     |
| LIQUOR LAW VIOLATIONS                                  | 0.737     | 0.767  | 0.751    | 214     |
| MANSLAUGHTER - NON-VEHICULAR                           | 0.653     | 0.796  | 0.717    | 139     |
| MANSLAUGHTER - VEHICULAR                               | 0.741     | 0.835  | 0.784    | 117     |
| MARIJUANA/HASHISH VIOLATION - OFFENSE UNSPECIFIED      | 0.796     | 0.649  | 0.712    | 62      |
| MISDEMEANOR UNSPECIFIED                                | 0.551     | 0.238  | 0.329    | 57      |
| MORALS/DECENCY - OFFENSE                               | 0.766     | 0.759  | 0.762    | 412     |
| MURDER                                                 | 0.965     | 0.915  | 0.939    | 621     |
| OBSTRUCTION - LAW ENFORCEMENT                          | 0.939     | 0.946  | 0.943    | 4214    |
| OFFENSES AGAINST COURTS, LEGISLATURES, AND COMMISSIONS | 0.891     | 0.894  | 0.893    | 1965    |
| PAROLE VIOLATION                                       | 0.97      | 0.957  | 0.963    | 946     |
| PETTY LARCENY - THEFT UNDER $200                       | 0.967     | 0.599  | 0.739    | 175     |
| POSSESSION/USE - COCAINE OR CRACK                      | 0.878     | 0.903  | 0.889    | 68      |
| POSSESSION/USE - DRUG UNSPECIFIED                      | 0.617     | 0.548  | 0.58     | 189     |
| POSSESSION/USE - HEROIN                                | 0.899     | 0.852  | 0.873    | 25      |
| POSSESSION/USE - MARIJUANA/HASHISH                     | 0.973     | 0.971  | 0.972    | 556     |
| POSSESSION/USE - OTHER CONTROLLED SUBSTANCES           | 0.974     | 0.966  | 0.97     | 3271    |
| PROBATION VIOLATION                                    | 0.967     | 0.951  | 0.959    | 1158    |
| PROPERTY OFFENSES - OTHER                              | 0.887     | 0.869  | 0.878    | 446     |
| PUBLIC ORDER OFFENSES - OTHER                          | 0.693     | 0.724  | 0.708    | 1871    |
| RACKETEERING/EXTORTION (FEDERAL ONLY)                  | 0         | 0      | 0        | 2       |
| RAPE - FORCE                                           | 0.841     | 0.872  | 0.856    | 641     |
| RAPE - STATUTORY - NO FORCE                            | 0.705     | 0.623  | 0.648    | 140     |
| REGULATORY OFFENSES (FEDERAL ONLY)                     | 0.786     | 0.58   | 0.666    | 70      |
| RIOTING                                                | 0.759     | 0.588  | 0.66     | 119     |
| SEXUAL ASSAULT - OTHER                                 | 0.832     | 0.833  | 0.832    | 971     |
| SIMPLE ASSAULT                                         | 0.978     | 0.964  | 0.971    | 4577    |
| STOLEN PROPERTY - RECEIVING                            | 0.958     | 0.959  | 0.958    | 1193    |
| STOLEN PROPERTY - TRAFFICKING                          | 0.915     | 0.885  | 0.9      | 491     |
| TAX LAW (FEDERAL ONLY)                                 | 0.4       | 0.109  | 0.169    | 30      |
| TRAFFIC OFFENSES - MINOR                               | 0.969     | 0.976  | 0.972    | 8593    |
| TRAFFICKING - COCAINE OR CRACK                         | 0.898     | 0.946  | 0.922    | 185     |
| TRAFFICKING - DRUG UNSPECIFIED                         | 0.706     | 0.797  | 0.748    | 516     |
| TRAFFICKING - HEROIN                                   | 0.893     | 0.926  | 0.909    | 54      |
| TRAFFICKING - OTHER CONTROLLED SUBSTANCES              | 0.957     | 0.948  | 0.952    | 2937    |
| TRAFFICKING MARIJUANA/HASHISH                          | 0.92      | 0.941  | 0.93     | 255     |
| TRESPASSING                                            | 0.974     | 0.98   | 0.977    | 1916    |
| UNARMED ROBBERY                                        | 0.938     | 0.937  | 0.938    | 377     |
| UNAUTHORIZED USE OF VEHICLE                            | 0.921     | 0.918  | 0.919    | 304     |
| UNSPECIFIED HOMICIDE                                   | 0.603     | 0.557  | 0.578    | 60      |
| VIOLENT OFFENSES - OTHER                               | 0.816     | 0.825  | 0.82     | 606     |
| VOLUNTARY/NONNEGLIGENT MANSLAUGHTER                    | 0.662     | 0.577  | 0.613    | 54      |
| WEAPON OFFENSE                                         | 0.935     | 0.947  | 0.941    | 2441    |

*Note: `support` is the average number of observations per fold, so the total number of observations per class is roughly 3x support.*