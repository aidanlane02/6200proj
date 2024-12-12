Evolutionary model v2 is the final model that we used to generate and graph results
Evolutionary model v1 was used to generate test results but does not create graphs

The below files are dependencies of Evolutionary model v2 and must be ran prior to running evolutionary model v2:
SAR model v3 is our most up to date fish model which first trains the model and then has a function defined that takes in parameters and outputs predicted SAR
WTT calculates water transit time given which dams are breached and river conditions
Hydro Flow Adjustments adjusts flow and water elevation given which dams are breached
Spill Adjuster adjusts spill given a minimum spill percent
Economics model v1 is our economics model which sums energy replacement cost, breach cost, and transportation cost
Freight model generates transportation cost given which dams are breached
Hydromodel v2 generates hydropower output given flow rates

All other files are not needed for the final evolutionary model to work, they are a mix of previous versions, files used to test, and files used to clean data
