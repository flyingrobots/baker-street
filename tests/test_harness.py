import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('baker_eval',ROOT/'evals/run.py')
evalmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(evalmod)

def synthetic_response(case_id):
    """Hand-built contract control; not an agent result or semantic oracle."""
    item,source=evalmod.get_case(case_id)
    expected=evalmod.read_json(source/'oracle.json')
    claims=[]
    for cid,c in expected['claims'].items():
        lines=c.get('evidence_lines',[1])
        claims.append({'id':cid,'assessment':c['assessment'][0], 'basis':['SOURCE'],
                       'evidence':[{'path':c['evidence_path'],'start':min(lines),'end':max(lines)}],
                       'rationale':'Synthetic control for the grader only.', 'limits':'Not an agent or semantic result.'})
    findings=[]
    for i,f in enumerate(expected['required_findings'],1):
        claim=next(c for c in claims if c['id']==f['claim_id'])
        findings.append({'id':f'F{i}','claim_ids':[f['claim_id']],'status':f['status'],
                         'severity':f.get('severity',['HIGH'])[0], 'origin':'UNKNOWN',
                         'disposition':f['disposition'],'impact':'Synthetic contract control.', 'evidence':claim['evidence']})
    result={'decision':expected['decisions'][0],'claims':claims,'findings':findings,
            'limits':['Synthetic grader control only.'],'next_action':'Perform semantic review separately.'}
    if expected.get('probe_triage'):
        result['probe_triage']=[{'id':pid,'disposition':disposition,
            'rationale':'Synthetic control only.',
            'evidence':[{'path':'input/inventory.md','start':i,'end':i}]}
            for i,(pid,disposition) in enumerate(expected['probe_triage'].items(),1)]
    return result

class HarnessTests(unittest.TestCase):
    def good(self,cid='case-01'):
        r=synthetic_response(cid)
        self.assertEqual(evalmod.grade(cid,r)['contract_status'],'PASS')
        return r
    def bad(self,r,cid='case-01'):
        self.assertEqual(evalmod.grade(cid,r)['contract_status'],'FAIL')
    def test_all_synthetic_controls(self):
        for c in evalmod.catalog():
            with self.subTest(case=c['id']): self.good(c['id'])
    def test_unknown_severity_is_representable(self):
        r=self.good('case-17')
        r['findings'].append({'id':'Funknown','claim_ids':['C1'],'status':'HYPOTHESIS',
            'severity':'UNKNOWN','origin':'UNKNOWN','disposition':'INVESTIGATE',
            'impact':'Consequences have not been established.', 'evidence':r['claims'][0]['evidence']})
        self.assertEqual(evalmod.grade('case-17',r)['contract_status'],'PASS')
    def test_probe_misclassification(self):
        r=self.good('case-16');r['probe_triage'][2]['disposition']='ARCHIVE';self.bad(r,'case-16')
    def test_probe_missing(self):
        r=self.good('case-16');r['probe_triage'].pop();self.bad(r,'case-16')
    def test_probe_duplicate(self):
        r=self.good('case-16');r['probe_triage'].append(copy.deepcopy(r['probe_triage'][0]));self.bad(r,'case-16')
    def test_wrong_decision(self):
        r=self.good();r['decision']='BLOCKED';self.bad(r)
    def test_hypothesis_promotion(self):
        r=self.good('case-03');r['claims'][0]['assessment']='SUPPORTED';self.bad(r,'case-03')
    def test_claim_omission(self):
        r=self.good();r['claims'].pop();self.bad(r)
    def test_duplicate_claim(self):
        r=self.good();r['claims'].append(copy.deepcopy(r['claims'][0]));self.bad(r)
    def test_missing_evidence(self):
        r=self.good();r['claims'][0]['evidence']=[];self.bad(r)
    def test_invented_evidence(self):
        r=self.good();r['claims'][0]['evidence'][0]['path']='input/nonexistent';self.bad(r)
    def test_evidence_path_escape(self):
        r=self.good();r['claims'][0]['evidence'][0]['path']='input/../oracle.json';self.bad(r)
    def test_invalid_line(self):
        r=self.good();r['claims'][0]['evidence'][0]['end']=999;self.bad(r)
    def test_boolean_line_number(self):
        r=self.good();r['claims'][0]['evidence'][0]['start']=True;self.bad(r)
    def test_false_execution(self):
        r=self.good();r['claims'][0]['basis']=['EXECUTED'];self.bad(r)
    def test_unresolved_as_repair(self):
        r=self.good('case-02');r['findings'][0]['status']='HYPOTHESIS';self.bad(r,'case-02')
    def test_severity_downgrade_disclosed_loss(self):
        r=self.good('case-08');r['findings'][0]['severity']='INFORMATIONAL';self.bad(r,'case-08')
    def open_finding(self,r,severity,disposition):
        return {'id':'Fopen','claim_ids':['C1'],'status':'CONFIRMED','severity':severity,
                'origin':'UNKNOWN','disposition':disposition,'impact':'Synthetic severity control.',
                'evidence':r['claims'][0]['evidence']}
    def test_open_critical_or_high_prevents_ready_whatever_disposition(self):
        for severity in ('CRITICAL','HIGH'):
            for disposition in ('FOLLOW_UP','ACCEPTED','INVESTIGATE','REQUIRED_REPAIR'):
                with self.subTest(severity=severity,disposition=disposition):
                    r=self.good('case-23');r['findings']=[self.open_finding(r,severity,disposition)]
                    errors=evalmod.grade('case-23',r)['errors']
                    self.assertTrue(any(f'open {severity}' in e for e in errors),errors)
    def test_accepted_high_needs_recorded_user_acceptance_named_in_decision(self):
        r=self.good('case-23');f=self.open_finding(r,'HIGH','ACCEPTED');r['findings']=[f]
        r['limits']=['Fopen is accepted by the user; see acceptance record.']
        self.assertTrue(any('open HIGH' in e for e in evalmod.grade('case-23',r)['errors']))
        f['user_acceptance']='User accepted Fopen in the recorded acceptance criteria, basis: legacy clients only.'
        self.assertFalse(any('open HIGH' in e for e in evalmod.grade('case-23',r)['errors']))
        r['limits']=['Synthetic grader control only.']
        self.assertTrue(any('open HIGH' in e for e in evalmod.grade('case-23',r)['errors']))
    def test_user_acceptance_never_permits_ready_with_critical(self):
        r=self.good('case-23');f=self.open_finding(r,'CRITICAL','ACCEPTED')
        f['user_acceptance']='User accepted it.';r['findings']=[f];r['limits']=['Fopen accepted.']
        self.assertTrue(any('open CRITICAL' in e for e in evalmod.grade('case-23',r)['errors']))
    def test_withdrawn_high_does_not_prevent_ready(self):
        r=self.good('case-23');f=self.open_finding(r,'HIGH','ACCEPTED');f['status']='WITHDRAWN'
        r['findings']=[f]
        self.assertFalse(any('open HIGH' in e for e in evalmod.grade('case-23',r)['errors']))
    def finding_errors(self,cid,r,fid='Fopen'):
        return [e for e in evalmod.grade(cid,r)['errors'] if e.startswith(f'{fid}:')]
    def test_low_and_informational_follow_up_are_valid_with_ready(self):
        # case-23 is a clean case, so its only expected error is the active-finding cap.
        for severity in ('LOW','INFORMATIONAL'):
            with self.subTest(severity=severity):
                r=self.good('case-23');r['findings']=[self.open_finding(r,severity,'FOLLOW_UP')]
                self.assertEqual(evalmod.grade('case-23',r)['errors'],
                                 ['Active findings exceed this clean-case contract.'])
    def test_low_required_repair_left_to_checker(self):
        r=self.good('case-21');r['findings'].append(self.open_finding(r,'LOW','REQUIRED_REPAIR'))
        self.assertEqual(self.finding_errors('case-21',r),[])
    def test_informational_cannot_be_required_repair(self):
        r=self.good('case-21');r['findings'].append(self.open_finding(r,'INFORMATIONAL','REQUIRED_REPAIR'))
        errors=self.finding_errors('case-21',r)
        self.assertTrue(any('INFORMATIONAL' in e and 'required repair' in e for e in errors),errors)
    def test_withdrawn_finding_keeps_its_rule(self):
        r=self.good('case-21');f=self.open_finding(r,'INFORMATIONAL','REQUIRED_REPAIR');f['status']='WITHDRAWN'
        r['findings'].append(f)
        self.assertTrue(any('withdrawn' in e for e in self.finding_errors('case-21',r)))
        f['disposition']='ACCEPTED'
        self.assertEqual(self.finding_errors('case-21',r),[])
    def adverse_consequence_rule(self):
        text=(ROOT/'references/records.md').read_text(encoding='utf-8')
        start=text.index('Adverse consequence:')
        return ' '.join(text[start:text.index('\n\n',start)].split())
    def test_follow_up_fallback_keeps_unconfirmed_dispositions(self):
        # The grader requires WITHDRAWN to be ACCEPTED; the rule must not send it to FOLLOW_UP.
        rule=self.adverse_consequence_rule()
        self.assertIn('A CONFIRMED finding that fails this rule is FOLLOW_UP',rule)
        self.assertIn('WITHDRAWN is ACCEPTED',rule)
        self.assertIn('INVESTIGATE',rule)
    def test_watson_lets_a_violated_criterion_justify_a_required_repair(self):
        # Condition (a) alone suffices in records; Watson must not demote such a repair.
        text=' '.join((ROOT/'roles/watson.md').read_text(encoding='utf-8').split())
        start=text.index('When you propose that a DOC, CHANGELOG or PR_BODY repair is required')
        sentence=text[start:text.index('Separate investigation',start)]
        self.assertNotIn('otherwise it is a batched FOLLOW_UP',sentence)
        self.assertIn('acceptance criterion',sentence)
        self.assertIn('adverse-consequence rule in records',sentence)
    def test_none_basis_combination(self):
        r=self.good();r['claims'][0]['basis']=['NONE','SOURCE'];self.bad(r)
    def test_malformed_values(self):
        for value in [None,[],5,'text',{}]: self.bad(value)
    def test_malformed_claim_and_finding(self):
        r=self.good();r['claims']=[None];r['findings']=[[]];self.bad(r)
    def test_non_scalar_enum_values(self):
        for value in [[], {}, True, 42]:
            r=self.good();r['decision']=value;self.bad(r)
            r=self.good();r['claims'][0]['assessment']=value;self.bad(r)
            r=self.good('case-02');r['findings'][0]['status']=value;self.bad(r,'case-02')
    def test_clean_case_false_positive(self):
        r=self.good();r['findings']=[{'id':'F1','claim_ids':['C1'],'status':'CONFIRMED',
        'severity':'LOW','origin':'UNKNOWN','disposition':'FOLLOW_UP','impact':'Manufactured nit.',
        'evidence':r['claims'][0]['evidence']}];self.bad(r)
    def test_semantic_status_never_auto_passes(self):
        self.assertEqual(evalmod.grade('case-01',self.good())['semantic_status'],'PENDING_HUMAN_REVIEW')
    def test_prepare_hides_oracle_and_titles(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'packet';evalmod.prepare('case-03',p)
            names={f.name for f in p.rglob('*')}
            self.assertNotIn('oracle.json',names);self.assertNotIn('catalog.json',names)
            self.assertNotIn('The unperformed experiment',(p/'TASK.md').read_text())
            self.assertEqual(evalmod.verify_packet('case-03',p),[])
    def test_modified_packet_detected_against_canonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'packet';evalmod.prepare('case-01',p)
            (p/'input/clamp.py').write_text('def clamp(x): return x\n')
            self.assertTrue(evalmod.verify_packet('case-01',p))
    def test_prepare_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): evalmod.prepare('case-01',tmp)
    def test_prepare_includes_modular_skill_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill=Path(tmp)/'skill';skill.mkdir();(skill/'SKILL.md').write_text('Entry point')
            for directory in ('references','roles','scripts'):
                (skill/directory).mkdir();(skill/directory/'example.txt').write_text(directory)
            packet=Path(tmp)/'packet';evalmod.prepare('case-01',packet,skill)
            for directory in ('references','roles','scripts'):
                self.assertEqual((packet/'skill'/directory/'example.txt').read_text(),directory)
    def test_unknown_case(self):
        with self.assertRaises(ValueError): evalmod.get_case('../../oracle')
    def test_boundary_fixture_truth(self):
        _,source=evalmod.get_case('case-02');ns={}
        exec((source/'input/validator.py').read_text(),ns)
        self.assertEqual(ns['validate'](9),9)
        with self.assertRaises(ValueError): ns['validate'](10)
    def test_faulty_fixture_is_not_used_as_control(self):
        _,source=evalmod.get_case('case-01');ns={}
        exec((source/'input/clamp.py').read_text(),ns)
        self.assertEqual([ns['clamp'](i) for i in [-1,0,5,10,11]],[0,0,5,10,10])

if __name__=='__main__': unittest.main()
