import numpy as np
data_mu = float(35048)
data_el = float(27956)
ttbar_mu = float(40406)
ttbar_el = float(29964)
data_mu_tot = float(2475310)
data_el_tot = float(2192536)
ttbar_mu_tot = float(2191062)
ttbar_el_tot = float(2191062)

def div_err(x, ex, y, ey): # for x/y
	return np.sqrt(ex*ex/(y*y) + (x*x*ey*ey)/(y*y*y*y)  )

data_mu_eff = data_mu/data_mu_tot
data_el_eff = data_el/data_el_tot
ttbar_mu_eff = ttbar_mu/ttbar_mu_tot
ttbar_el_eff = ttbar_el/ttbar_el_tot
data_mu_eff_err = div_err(data_mu, np.sqrt(data_mu), data_mu_tot, np.sqrt(data_mu_tot))
data_el_eff_err = div_err(data_el, np.sqrt(data_el), data_el_tot, np.sqrt(data_el_tot))
ttbar_mu_eff_err = div_err(ttbar_mu, np.sqrt(ttbar_mu), ttbar_mu_tot, np.sqrt(ttbar_mu_tot))
ttbar_el_eff_err = div_err(ttbar_el, np.sqrt(ttbar_el), ttbar_el_tot, np.sqrt(ttbar_el_tot))

SF_mu = data_mu_eff/ttbar_mu_eff
SF_el = data_el_eff/ttbar_el_eff
SF_mu_err = div_err(data_mu_eff, data_mu_eff_err, ttbar_mu_eff, ttbar_mu_eff_err)
SF_el_err = div_err(data_el_eff, data_el_eff_err, ttbar_el_eff, ttbar_el_eff_err)

print SF_el, SF_el_err
print SF_mu, SF_mu_err