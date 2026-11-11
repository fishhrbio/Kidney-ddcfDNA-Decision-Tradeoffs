import ast
import base64
import hashlib
import json
from pathlib import Path
import tempfile
import shutil
import unittest
from run_analysis import unique_count,load_inputs,reconstruct,validate_rule_logic,rounding_sensitivity
class ScientificChecks(unittest.TestCase):
    def test_counts_and_predictive_values(self):
        s,_,_=load_inputs(); d,c=reconstruct(s)
        self.assertEqual(d[['TP','FN','TN','FP']].values.tolist(),[[14,1,32,3],[12,3,25,10],[15,0,23,12],[11,4,34,1]])
        self.assertTrue(c.matches_rounding.all())
    def test_wrong_predictive_value_fails(self):
        s,_,_=load_inputs(); s.loc[0,'ppv_percent']=90
        with self.assertRaisesRegex(ValueError,'ppv discrepancy'): reconstruct(s)
    def test_nonunique_or_impossible_counts_fail(self):
        for rate,n in [(50,100000),(50,3)]:
            with self.assertRaisesRegex(ValueError,'Nonunique/impossible'): unique_count(rate,n)
    def test_combined_rule_inconsistency_fails(self):
        s,_,_=load_inputs(); d,_=reconstruct(s); d.loc[2,'TP']=14
        with self.assertRaises(ValueError): validate_rule_logic(d)
    def test_rounding_choice(self):
        s,_,_=load_inputs(); self.assertTrue(rounding_sensitivity(s).unique_counts_unchanged.all())

    def test_notebook_recipe_matches_git_checkout(self):
        root = Path(__file__).resolve().parent
        notebook = json.loads((root / 'analysis.ipynb').read_text(encoding='utf-8'))
        first_code = next(c for c in notebook['cells'] if c['cell_type'] == 'code')
        assignments = {}
        for statement in ast.parse(''.join(first_code['source'])).body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    if isinstance(target, ast.Name) and target.id in {'PAYLOAD', 'EXPECTED'}:
                        assignments[target.id] = ast.literal_eval(statement.value)
        self.assertEqual(set(assignments), {'PAYLOAD', 'EXPECTED'})
        self.assertEqual(set(assignments['PAYLOAD']), set(assignments['EXPECTED']))
        for relative, encoded in assignments['PAYLOAD'].items():
            with self.subTest(path=relative):
                embedded = base64.b64decode(encoded)
                actual = (root / relative).read_bytes()
                self.assertEqual(embedded, actual)
                self.assertEqual(hashlib.sha256(actual).hexdigest(), assignments['EXPECTED'][relative])
                # Git leaves CSV bytes untouched; other recipe files use LF.
                if not relative.endswith('.csv'):
                    self.assertNotIn(b'\r\n', actual)

    def test_changed_source_bytes_are_rejected(self):
        root = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory)
            shutil.copyfile(root / 'INPUT_MANIFEST.json', copied / 'INPUT_MANIFEST.json')
            shutil.copytree(root / 'data/published_summary', copied / 'data/published_summary')
            source = copied / 'data/published_summary/diagnostic_performance.csv'
            source.write_bytes(source.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'Input checksum mismatch'):
                load_inputs(copied)
if __name__=='__main__': unittest.main()
