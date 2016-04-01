import numpy as np
import rebound

class State(object):

    def __init__(self, planets):
        self.planets = planets


    def setup_sim(self):
        sim = rebound.Simulation()
        sim.add(m=1.)
        for planet in self.planets:
            sim.add(**planet)
        sim.move_to_com()
        return sim

    def get_rv(self, times):
        sim = self.setup_sim()
        
        rv = np.zeros(len(times))
        for i, t in enumerate(times):
            sim.integrate(t)
            rv[i] = sim.particles[0].vx

        return rv

    def get_rv_plotting(self, Npoints=200, tmax=1.5):
        times = np.linspace(0,tmax,Npoints)
        return times, self.get_rv(times)


    def get_chi2(self, obs):
        rv = self.get_rv(obs.t)
        chi2 = 0.
        for i, t in enumerate(obs.t):
            chi2 += (rv[i]-obs.rv[i])**2
        return chi2/(obs.error**2 * obs.Npoints)

class StateVar(State):

    def __init__(self, planets, ignore_vars=[]):
        super(StateVar,self).__init__(planets)
        self.planets_vars = []
        self.Nvars = 0
        for planet in planets:
            planet_vars = [x for x in planet.keys() if x not in ignore_vars]
            self.planets_vars.append(planet_vars)
            self.Nvars += len(planet_vars)

    def var_pindex_vname(self, vindex):
        vi = 0.
        for pindex, p in enumerate(self.planets_vars):
            for v in p:
                if vindex == vi:
                    return pindex+1, v
                vi += 1


    def setup_sim_vars(self):
        sim = super(StateVar,self).setup_sim()
        variations1 = []
        variations2 = []
        for vindex in range(self.Nvars):
            pindex, vname = self.var_pindex_vname(vindex)
            v = sim.add_variation(order=1)
            v.vary_pal(pindex,vname)
            variations1.append(v)
        
        for vindex1 in range(self.Nvars):
            for vindex2 in range(self.Nvars):
                if vindex1 >= vindex2:
                    pindex1, vname1 = self.var_pindex_vname(vindex1)
                    pindex2, vname2 = self.var_pindex_vname(vindex2)
                    v = sim.add_variation(order=2, first_order=variations1[vindex1], first_order_2=variations1[vindex2])
                    if pindex1 == pindex2:
                        v.vary_pal(pindex1,vname1,vname2)
                    variations2.append(v)

        sim.move_to_com()
        return sim, variations1, variations2

    def get_chi2_d_dd(self, obs):
        sim, variations1, variations2 = self.setup_sim_vars()
        chi2 = 0.
        chi2_d = np.zeros(self.Nvars)
        chi2_dd = np.zeros((self.Nvars,self.Nvars))
        normfac = 1./(obs.error**2 * obs.Npoints)
        for i, t in enumerate(obs.t):
            sim.integrate(t)
            chi2 += (sim.particles[0].vx-obs.rv[i])**2*normfac
            v2index = 0
            for vindex1 in range(self.Nvars):
                chi2_d[vindex1] += 2. * variations1[vindex1].particles[0].vx * (sim.particles[0].vx-obs.rv[i])*normfac
            
                for vindex2 in range(self.Nvars):
                    if vindex1 >= vindex2:
                        chi2_dd[vindex1][vindex2] +=  2. * variations2[v2index].particles[0].vx * (sim.particles[0].vx-obs.rv[i])*normfac + 2. * variations1[vindex1].particles[0].vx * variations1[vindex2].particles[0].vx*normfac
                        v2index += 1
                        chi2_dd[vindex2][vindex1] = chi2_dd[vindex1][vindex2]

        return chi2, chi2_d, chi2_dd


