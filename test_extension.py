import unittest
import numpy as np
import pandas as pd
from stability import reachable_states, simulate, audit_samples, classify, STATES, independent_envelope_states
from molecular import validate_metadata, module_scores, association_estimates

class StabilityChecks(unittest.TestCase):
    def test_zero_bounds_and_boundary(self):
        self.assertEqual(reachable_states(1,1,1,1),['both_high'])
        self.assertEqual(reachable_states(.5,2,1,1),['absolute_only_high'])
        self.assertEqual(reachable_states(1,1,1,1,.1,.1),STATES)

    def test_exact_open_boundaries(self):
        # If T has no error and both normalized measurements coincide,
        # two discordant states are impossible under shared fraction error.
        self.assertEqual(reachable_states(1,1,1,1,.2,0),['both_low','both_high'])

    def test_dense_grid_agrees_away_from_boundary(self):
        for f,d in [(.7,.9),(1.1,.6),(.8,1.4),(1.7,1.4)]:
            x,y=np.meshgrid(np.linspace(-.3,.3,501),np.linspace(-.2,.2,501))
            sampled=set(STATES[i] for i in np.unique(classify(f*np.exp(x),d*np.exp(x+y),1,1)))
            self.assertEqual(set(reachable_states(f,d,1,1,.3,.2)),sampled)

    def test_larger_bounds_cannot_remove_states(self):
        for f in [.5,.9,1.,1.1,2.]:
            for d in [.5,.9,1.,1.1,2.]:
                self.assertTrue(set(reachable_states(f,d,1,1,.1,.1))<=set(reachable_states(f,d,1,1,.4,.4)))

    def test_independent_envelope_contains_coupled_states(self):
        for f in [.5,.9,1.,1.1,2.]:
            for d in [.5,.9,1.,1.1,2.]:
                for a,b in [(.1,0),(.2,.1),(0,.1)]:
                    self.assertTrue(set(reachable_states(f,d,1,1,a,b))<=set(independent_envelope_states(f,d,1,1,a,b)))
        self.assertEqual(len(independent_envelope_states(1,1,1,1,.2,0)),4)
        self.assertEqual(len(reachable_states(1,1,1,1,.2,0)),2)

    def test_simulated_support_and_reproducibility(self):
        p=simulate(1,1,1,1,.2,0,n=10000)
        self.assertEqual(p,simulate(1,1,1,1,.2,0,n=10000))
        self.assertEqual(p['fraction_only_high'],0.)
        self.assertEqual(p['absolute_only_high'],0.)
        self.assertAlmostEqual(sum(p.values()),1.)

    def test_physical_fraction_and_invalid_values(self):
        self.assertEqual(reachable_states(100,1,100,1,.1,0),['both_low','both_high'])
        for f in [0,101,np.nan,np.inf]:
            with self.assertRaises(ValueError): reachable_states(f,1,1,1,.1,.1)
        with self.assertRaises(ValueError): reachable_states(1,1,1,1,-.1,.1)

    def test_duplicate_and_missing_sample_rejected(self):
        f=pd.DataFrame(dict(sample_id=['a','a'],fraction_percent=[1,1],absolute_copies_ml=[1,1]))
        with self.assertRaises(ValueError):audit_samples(f,1,1,.1,.1)

class MolecularChecks(unittest.TestCase):
    def metadata(self):
        return pd.DataFrame(dict(sample_id=list('abcdef'),patient_id=list('abcdef'),partition=['discovery']*3+['validation']*3,fraction_percent=[1.]*6,absolute_copies_ml=[2.]*6,assay=['test']*6,phenotype=['test']*6))

    def test_patient_leakage_rejected(self):
        m=self.metadata(); m.loc[3,'patient_id']='a'
        with self.assertRaisesRegex(ValueError,'leakage'):validate_metadata(m)

    def test_training_only_normalization(self):
        m=self.metadata(); x=pd.DataFrame([[1,2,3,4,5,6]],index=['GENE'],columns=list('abcdef'))
        z=module_scores(x,m,{'module':['GENE']})
        self.assertAlmostEqual(z.loc['a','module'],-1)
        self.assertAlmostEqual(z.loc['f','module'],4)
        x.loc['GENE','f']=10000
        self.assertAlmostEqual(module_scores(x,m,{'module':['GENE']}).loc['a','module'],-1)

    def test_missing_gene_and_zero_variance_fail(self):
        m=self.metadata(); x=pd.DataFrame([[1]*6],index=['GENE'],columns=list('abcdef'))
        with self.assertRaisesRegex(ValueError,'Missing'):module_scores(x,m,{'module':['absent']})
        with self.assertRaisesRegex(ValueError,'variance'):module_scores(x,m,{'module':['GENE']})

    def test_known_linear_coefficients_recovered(self):
        rng=np.random.default_rng(5); n=80
        m=pd.DataFrame(dict(sample_id=[f's{i}' for i in range(n)],patient_id=[f'p{i}' for i in range(n)],partition=['discovery']*40+['validation']*40,fraction_percent=np.exp(rng.uniform(-2,0,n)),absolute_copies_ml=np.exp(rng.uniform(0,3,n)),assay=['test']*n,phenotype=['test']*n))
        scores=pd.DataFrame({'known':2*np.log(m.fraction_percent.to_numpy())-3*np.log(m.absolute_copies_ml.to_numpy())},index=m.sample_id)
        out=association_estimates(scores,m,replicates=2000)
        for r in out.itertuples():self.assertAlmostEqual(r.estimate,2 if r.predictor=='log_fraction' else -3)

if __name__=='__main__':unittest.main()
