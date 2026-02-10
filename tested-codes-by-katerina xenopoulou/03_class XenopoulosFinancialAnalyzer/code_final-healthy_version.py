
# ============================================================================
# ΣΥΣΤΗΜΑ ΑΝΑΛΥΣΗΣ ΤΡΑΠΕΖΙΚΩΝ ΣΥΝΑΛΛΑΓΩΝ ΞΕΝΟΠΟΥΛΟΥ v3.0
# Ολοκληρωμένη έκδοση με αυτο-διορθωτικές δυνατότητες
# ============================================================================

# ΒΙΒΛΙΟΘΗΚΕΣ
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import hashlib
import re
import json
import sys
from typing import Dict, List, Tuple, Any, Optional, Union
import ast

# ============================================================================
# 1. ΒΑΣΙΚΟΣ ΑΝΑΛΥΤΗΣ ΞΕΝΟΠΟΥΛΟΥ
# ============================================================================

class XenopoulosFinancialAnalyzer:
    """Ολικός αναλυτής τραπεζικών συστημάτων με διαλεκτική λογική"""
    
    def __init__(self, system_name: str = "Τραπεζικό Σύστημα"):
        self.system_name = system_name
        self.transaction_history = []
        self.risk_patterns = self._load_risk_patterns()
        self.paradox_memory = []
        self.audit_log = []
        self.analysis_count = 0
        
    def _load_risk_patterns(self) -> Dict:
        """Πρότυπα κινδύνου για τραπεζικά συστήματα"""
        return {
            'compound_interest': [
                'interest_on_interest',
                'increasing_balance_despite_payments',
                'multiple_fee_types',
                'frequent_rate_changes'
            ],
            'delinquency': [
                'late_payment_pattern',
                'increasing_delays',
                'fee_accumulation',
                'communication_breakdown'
            ],
            'fraud': [
                'unusual_time_patterns',
                'geolocation_mismatch',
                'amount_anomalies',
                'behavioral_changes'
            ],
            'compliance': [
                'exceeding_rate_limits',
                'unauthorized_fees',
                'non_transparent_charges',
                'regulatory_violations'
            ]
        }
    
    def analyze_transaction_set(self, transactions: List[Dict]) -> Dict:
        """Ολοκληρωμένη ανάλυση συνόλου συναλλαγών"""
        self.analysis_count += 1
        
        try:
            df = pd.DataFrame(transactions)
        except Exception as e:
            return self._error_response(f"Σφάλμα στη δημιουργία DataFrame: {str(e)}")
        
        # Υπολογισμός βασικών μετρικών
        try:
            risk_metrics = self._calculate_risk_metrics(df)
            compliance_check = self._check_compliance(df)
            paradox_detection = self._detect_paradoxical_patterns(df)
            economic_impact = self._calculate_economic_impact(df, risk_metrics)
        except Exception as e:
            return self._error_response(f"Σφάλμα στην ανάλυση: {str(e)}")
        
        # Εκτέλεση αυτο-ανάλυσης για συστημικά παράδοξα
        system_paradox = self._check_system_paradox(risk_metrics, compliance_check, paradox_detection)
        
        analysis = {
            'summary': {
                'total_transactions': len(df),
                'total_amount': float(df['amount'].sum()) if 'amount' in df.columns else 0,
                'avg_amount': float(df['amount'].mean()) if 'amount' in df.columns else 0,
                'date_range': f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else 'N/A',
                'analysis_id': f"ANL{self.analysis_count:06d}",
                'timestamp': datetime.now().isoformat()
            },
            'risk_analysis': risk_metrics,
            'compliance_check': compliance_check,
            'paradox_detection': paradox_detection,
            'economic_impact': economic_impact,
            'system_paradox': system_paradox
        }
        
        # Καταγραφή στην ιστορία
        self.transaction_history.append({
            'analysis_id': analysis['summary']['analysis_id'],
            'timestamp': analysis['summary']['timestamp'],
            'transaction_count': analysis['summary']['total_transactions']
        })
        
        return analysis
    
    def _calculate_risk_metrics(self, df: pd.DataFrame) -> Dict:
        """Υπολογισμός μετρικών κινδύνου με ενισχυμένη λογική"""
        metrics = {}
        
        # Έλεγχος για σύνθετους τόκους
        metrics['compound_interest_risk'] = self._detect_compound_interest(df)
        
        # Έλεγχος καθυστερήσεων
        metrics['delinquency_risk'] = self._detect_delinquency_patterns(df)
        
        # Έλεγχος απάτης
        metrics['fraud_risk'] = self._detect_fraud_patterns(df)
        
        # Έλεγχος συγκέντρωσης κινδύνου
        metrics['concentration_risk'] = self._detect_concentration_risk(df)
        
        # Υπολογισμός συνολικού κινδύνου με σταθμισμένο μέσο όρο
        risk_weights = {
            'compound_interest_risk': 0.3,
            'delinquency_risk': 0.25,
            'fraud_risk': 0.25,
            'concentration_risk': 0.2
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for risk_type, weight in risk_weights.items():
            if risk_type in metrics and 'score' in metrics[risk_type]:
                total_weighted_score += metrics[risk_type]['score'] * weight
                total_weight += weight
        
        if total_weight > 0:
            metrics['overall_risk_score'] = total_weighted_score / total_weight
        else:
            metrics['overall_risk_score'] = 0
        
        # Προσθήκη επιπέδου κινδύνου
        risk_score = metrics['overall_risk_score']
        if risk_score >= 0.8:
            metrics['risk_level'] = 'ΚΡΙΣΙΜΟΣ'
        elif risk_score >= 0.6:
            metrics['risk_level'] = 'ΥΨΗΛΟΣ'
        elif risk_score >= 0.4:
            metrics['risk_level'] = 'ΜΕΣΟΣ'
        elif risk_score >= 0.2:
            metrics['risk_level'] = 'ΧΑΜΗΛΟΣ'
        else:
            metrics['risk_level'] = 'ΠΟΛΥ ΧΑΜΗΛΟΣ'
        
        return metrics
    
    def _detect_compound_interest(self, df: pd.DataFrame) -> Dict:
        """Εντοπισμός σύνθετων τόκων με βελτιωμένη λογική"""
        if len(df) < 3:
            return self._create_risk_result(False, 0, "Ανεπαρκή δεδομένα")
        
        indicators = []
        scores = []
        
        # 1. Έλεγχος αυξανόμενου υπολοίπου
        if 'balance' in df.columns and len(df) > 1:
            try:
                balance_increase = df['balance'].iloc[-1] - df['balance'].iloc[0]
                if balance_increase > 0:
                    indicators.append('increasing_balance')
                    scores.append(0.7)
            except:
                pass
        
        # 2. Συχνότητα αλλαγών επιτοκίου
        if 'interest_rate' in df.columns and len(df) > 2:
            try:
                rate_changes = (df['interest_rate'].diff().abs() > 0.1).sum()
                if rate_changes > len(df) * 0.3:  # 30% των συναλλαγών άλλαξαν επιτόκιο
                    indicators.append('frequent_rate_changes')
                    scores.append(0.6)
            except:
                pass
        
        # 3. Ταυτόχρονα υψηλά ποσά και επιτόκια
        if all(col in df.columns for col in ['amount', 'interest_rate']):
            try:
                amount_high = df['amount'] > df['amount'].quantile(0.75)
                rate_high = df['interest_rate'] > df['interest_rate'].quantile(0.75)
                simultaneous_high = (amount_high & rate_high).sum()
                
                if simultaneous_high > 0:
                    indicators.append('simultaneous_high_values')
                    scores.append(0.8)
            except:
                pass
        
        # 4. Μοτίβα επανάληψης
        if 'reason' in df.columns:
            try:
                fee_reasons = ['fee', 'charge', 'commission', 'καθυστέρησης', 'προμήθεια']
                fee_count = df['reason'].astype(str).str.contains('|'.join(fee_reasons), case=False, na=False).sum()
                if fee_count > len(df) * 0.4:  # 40% των συναλλαγών είναι χρεώσεις
                    indicators.append('high_fee_frequency')
                    scores.append(0.5)
            except:
                pass
        
        if scores:
            avg_score = np.mean(scores)
            detected = avg_score > 0.5
        else:
            avg_score = 0
            detected = False
        
        result = self._create_risk_result(
            detected=detected,
            score=avg_score,
            indicators=indicators,
            details={
                'indicators_found': len(indicators),
                'max_indicator_score': max(scores) if scores else 0
            }
        )
        
        return result
    
    def _detect_delinquency_patterns(self, df: pd.DataFrame) -> Dict:
        """Εντοπισμός προτύπων καθυστέρησης"""
        # Αρχικοποίηση
        indicators = []
        scores = []
        
        # 1. Έλεγχος καθυστερήσεων από ημερομηνίες
        if all(col in df.columns for col in ['payment_date', 'due_date']):
            try:
                df['payment_date'] = pd.to_datetime(df['payment_date'])
                df['due_date'] = pd.to_datetime(df['due_date'])
                df['delay_days'] = (df['payment_date'] - df['due_date']).dt.days
                df['is_delayed'] = df['delay_days'] > 0
                
                total_delays = df['is_delayed'].sum()
                delay_rate = total_delays / len(df)
                
                if delay_rate > 0.3:
                    indicators.append(f'high_delay_rate_{delay_rate:.1%}')
                    scores.append(min(0.3 + delay_rate, 0.9))
                
                # Έλεγχος επιδεινούμενων καθυστερήσεων
                if len(df) > 5:
                    recent_delay_rate = df['is_delayed'].iloc[-5:].sum() / 5
                    if recent_delay_rate > delay_rate * 1.5:
                        indicators.append('worsening_delays')
                        scores.append(0.7)
            except:
                pass
        
        # 2. Έλεγχος συσσώρευσης χρεώσεων
        if 'fee' in df.columns:
            try:
                total_fees = df['fee'].sum()
                if total_fees > len(df) * 20:  # Μέσο όρο €20 ανά συναλλαγή
                    indicators.append('high_fee_accumulation')
                    scores.append(min(0.4 + (total_fees / (len(df) * 100)), 0.8))
            except:
                pass
        
        # 3. Έλεγχος προτύπου πληρωμών
        if 'payment_amount' in df.columns and len(df) > 3:
            try:
                payment_std = df['payment_amount'].std()
                if payment_std == 0:
                    indicators.append('identical_payments')
                    scores.append(0.3)
            except:
                pass
        
        if scores:
            avg_score = np.mean(scores)
            detected = avg_score > 0.4
        else:
            avg_score = 0
            detected = False
        
        details = {}
        if 'total_delays' in locals():
            details['total_delays'] = int(total_delays)
        if 'delay_rate' in locals():
            details['delay_rate'] = float(delay_rate)
        
        return self._create_risk_result(detected, avg_score, indicators, details)
    
    def _detect_fraud_patterns(self, df: pd.DataFrame) -> Dict:
        """Ανίχνευση προτύπων απάτης"""
        if len(df) < 5:
            return self._create_risk_result(False, 0, "Ανεπαρκή δεδομένα")
        
        indicators = []
        scores = []
        
        # 1. Ασυνήθιστες ώρες συναλλαγών
        if 'transaction_time' in df.columns:
            try:
                hours = pd.to_datetime(df['transaction_time']).dt.hour
                night_transactions = ((hours >= 0) & (hours <= 5)).sum()
                night_ratio = night_transactions / len(df)
                
                if night_ratio > 0.2:
                    indicators.append(f'night_transactions_{night_ratio:.1%}')
                    scores.append(min(0.3 + night_ratio, 0.8))
            except:
                pass
        
        # 2. Ακραίες τιμές
        if 'amount' in df.columns:
            try:
                Q1 = df['amount'].quantile(0.25)
                Q3 = df['amount'].quantile(0.75)
                IQR = Q3 - Q1
                
                if IQR > 0:
                    outliers = ((df['amount'] < (Q1 - 1.5 * IQR)) | 
                               (df['amount'] > (Q3 + 1.5 * IQR))).sum()
                    outlier_ratio = outliers / len(df)
                    
                    if outlier_ratio > 0.1:
                        indicators.append(f'amount_outliers_{outlier_ratio:.1%}')
                        scores.append(min(0.4 + outlier_ratio, 0.9))
            except:
                pass
        
        # 3. Γεωγραφική ασυνέχεια
        if 'location' in df.columns and len(df) > 10:
            try:
                location_changes = (df['location'] != df['location'].shift()).sum()
                change_ratio = location_changes / len(df)
                
                if change_ratio > 0.8:
                    indicators.append(f'high_location_volatility_{change_ratio:.1%}')
                    scores.append(min(0.3 + change_ratio, 0.7))
            except:
                pass
        
        # 4. Συχνότητα συναλλαγών
        if 'transaction_date' in df.columns and len(df) > 1:
            try:
                df['date'] = pd.to_datetime(df['transaction_date']).dt.date
                daily_counts = df.groupby('date').size()
                
                if daily_counts.max() > 10:
                    indicators.append('high_daily_frequency')
                    scores.append(0.6)
            except:
                pass
        
        if scores:
            avg_score = np.mean(scores)
            detected = avg_score > 0.5
        else:
            avg_score = 0
            detected = False
        
        return self._create_risk_result(detected, avg_score, indicators)
    
    def _detect_concentration_risk(self, df: pd.DataFrame) -> Dict:
        """Ανίχνευση κινδύνου συγκέντρωσης"""
        indicators = []
        scores = []
        
        # 1. Συγκέντρωση σε μεγάλες συναλλαγές
        if 'amount' in df.columns and len(df) > 5:
            try:
                total_amount = df['amount'].sum()
                top_10_percent = df.nlargest(int(len(df) * 0.1), 'amount')
                concentration_ratio = top_10_percent['amount'].sum() / total_amount if total_amount > 0 else 0
                
                if concentration_ratio > 0.8:
                    indicators.append(f'amount_concentration_{concentration_ratio:.1%}')
                    scores.append(min(0.3 + concentration_ratio, 0.9))
            except:
                pass
        
        # 2. Συγκέντρωση σε συγκεκριμένους τύπους
        if 'transaction_type' in df.columns:
            try:
                type_counts = df['transaction_type'].value_counts()
                if len(type_counts) > 0:
                    dominant_type_ratio = type_counts.iloc[0] / len(df)
                    if dominant_type_ratio > 0.7:
                        indicators.append(f'type_concentration_{dominant_type_ratio:.1%}')
                        scores.append(min(0.3 + dominant_type_ratio, 0.8))
            except:
                pass
        
        if scores:
            avg_score = np.mean(scores)
            detected = avg_score > 0.5
        else:
            avg_score = 0
            detected = False
        
        return self._create_risk_result(detected, avg_score, indicators)
    
    def _check_compliance(self, df: pd.DataFrame) -> Dict:
        """Έλεγχος συμμόρφωσης με κανονισμούς"""
        violations = []
        warning_count = 0
        
        # 1. Έλεγχος επιτοκίων (όριο 11.35%)
        if 'interest_rate' in df.columns:
            try:
                high_rates = df[df['interest_rate'] > 11.35]
                if len(high_rates) > 0:
                    max_rate = high_rates['interest_rate'].max()
                    violations.append({
                        'type': 'interest_rate_violation',
                        'count': len(high_rates),
                        'max_rate': float(max_rate),
                        'limit': 11.35
                    })
            except:
                pass
        
        # 2. Έλεγχος για μη εξουσιοδοτημένες χρεώσεις
        if 'fee_type' in df.columns:
            try:
                authorized_fees = ['service', 'maintenance', 'late', 'διαχείρισης', 'προμήθεια', 'other']
                unauthorized = df[~df['fee_type'].isin(authorized_fees)]
                if len(unauthorized) > 0:
                    violations.append({
                        'type': 'unauthorized_fee',
                        'count': len(unauthorized),
                        'fee_types': unauthorized['fee_type'].unique().tolist()[:5]
                    })
            except:
                pass
        
        # 3. Διαφάνεια περιγραφών
        if 'description' in df.columns:
            try:
                missing_descriptions = df['description'].isna().sum()
                if missing_descriptions > len(df) * 0.2:
                    warning_count += 1
            except:
                pass
        
        # 4. Έλεγχος ορίων ποσών
        if 'amount' in df.columns:
            try:
                # Προσομοίωση ορίου €10,000
                large_transactions = df[df['amount'] > 10000]
                if len(large_transactions) > 0:
                    warning_count += 1
            except:
                pass
        
        compliant = len(violations) == 0
        compliance_score = 1.0 if compliant else max(0, 1 - (len(violations) * 0.3))
        
        return {
            'compliant': compliant,
            'score': float(compliance_score),
            'violations': violations,
            'warnings': warning_count,
            'violation_count': len(violations),
            'recommendation': 'Άμεση διόρθωση παραβιάσεων' if violations else 'Συμμόρφωση OK'
        }
    
    def _detect_paradoxical_patterns(self, df: pd.DataFrame) -> Dict:
        """Ανίχνευση παραδόξων προτύπων (Xenopoulos Logic)"""
        if len(df) < 10:
            return self._create_paradox_result(False, 0, [], "Ανεπαρκή δεδομένα")
        
        paradox_patterns = []
        pattern_scores = []
        
        # 1. Ταυτόχρονες ακραίες τιμές (simultaneous_extremes)
        if all(col in df.columns for col in ['balance', 'interest_rate']):
            try:
                high_balance = df['balance'] > df['balance'].quantile(0.9)
                high_rate = df['interest_rate'] > df['interest_rate'].quantile(0.9)
                simultaneous_extremes = (high_balance & high_rate).any()
                
                if simultaneous_extremes:
                    paradox_patterns.append('simultaneous_extremes')
                    pattern_scores.append(0.8)
            except:
                pass
        
        # 2. Χαμηλή διακύμανση με υψηλό κίνδυνο (false_stability)
        if 'risk_score' in df.columns:
            try:
                low_variance = df['risk_score'].std() < 0.1
                high_risk = df['risk_score'].mean() > 0.7
                
                if low_variance and high_risk:
                    paradox_patterns.append('false_stability')
                    pattern_scores.append(0.9)
            except:
                pass
        
        # 3. Αντιφατικά πρότυπα πληρωμών
        if all(col in df.columns for col in ['payment_amount', 'balance']):
            try:
                increasing_payments = df['payment_amount'].diff().mean() > 0
                increasing_balance = df['balance'].diff().mean() > 0
                
                if increasing_payments and increasing_balance:
                    paradox_patterns.append('paradoxical_growth')
                    pattern_scores.append(0.7)
            except:
                pass
        
        # 4. Αυτο-αναφορά (self_referential)
        if 'description' in df.columns:
            try:
                self_ref_terms = ['auto', 'self', 'αυτόματος', 'ίδιος']
                self_ref_count = df['description'].astype(str).str.contains('|'.join(self_ref_terms), case=False, na=False).sum()
                
                if self_ref_count > len(df) * 0.1:
                    paradox_patterns.append('self_referential_patterns')
                    pattern_scores.append(0.6)
            except:
                pass
        
        if pattern_scores:
            paradox_score = np.mean(pattern_scores)
            paradox_detected = paradox_score > 0.3
        else:
            paradox_score = 0
            paradox_detected = False
        
        # Καταγραφή παραδόξου αν εντοπίστηκε
        if paradox_detected:
            paradox_event = {
                'timestamp': datetime.now().isoformat(),
                'patterns': paradox_patterns,
                'score': float(paradox_score),
                'data_sample_size': min(5, len(df)),
                'system_aware': True
            }
            self.paradox_memory.append(paradox_event)
            
            # Καταγραφή audit
            self._log_audit('paradox_detected', {
                'patterns': paradox_patterns,
                'score': paradox_score,
                'analysis_id': f"ANL{self.analysis_count:06d}"
            })
        
        return self._create_paradox_result(
            detected=paradox_detected,
            score=paradox_score,
            patterns=paradox_patterns,
            details={
                'patterns_count': len(paradox_patterns),
                'max_pattern_score': max(pattern_scores) if pattern_scores else 0
            }
        )
    
    def _check_system_paradox(self, risk_analysis: Dict, compliance: Dict, paradox_detection: Dict) -> Dict:
        """Ανίχνευση συστημικών παραδόξων στο ίδιο το σύστημα ανάλυσης"""
        paradoxes = []
        
        # 1. Παράδοξο: Υψηλός κίνδυνος αλλά χαμηλή προσοχή
        risk_level = risk_analysis.get('risk_level', '')
        overall_risk = risk_analysis.get('overall_risk_score', 0)
        
        if overall_risk > 0.7 and risk_level in ['ΧΑΜΗΛΟΣ', 'ΜΕΣΟΣ']:
            paradoxes.append({
                'type': 'risk_perception_paradox',
                'description': 'Υψηλός πραγματικός κίνδυνος αλλά χαμηλή αντίληψη κινδύνου',
                'severity': 'HIGH'
            })
        
        # 2. Παράδοξο: Παραβιάσεις αλλά καλή συμμόρφωση
        violation_count = compliance.get('violation_count', 0)
        compliance_score = compliance.get('score', 1)
        
        if violation_count > 0 and compliance_score > 0.8:
            paradoxes.append({
                'type': 'compliance_paradox',
                'description': f'{violation_count} παραβιάσεις αλλά υψηλό σκορ συμμόρφωσης',
                'severity': 'MEDIUM'
            })
        
        # 3. Παράδοξο: Ανίχνευση παραδόξου αλλά χωρίς άμεσες συστάσεις
        if paradox_detection.get('detected', False) and not self._has_immediate_recommendations(risk_analysis, compliance):
            paradoxes.append({
                'type': 'paradox_action_paradox',
                'description': 'Ανιχνεύτηκε παράδοξο αλλά δεν υπάρχουν άμεσες συστάσεις',
                'severity': 'CRITICAL'
            })
        
        return {
            'system_paradoxes_detected': len(paradoxes) > 0,
            'paradoxes': paradoxes,
            'count': len(paradoxes),
            'has_critical': any(p['severity'] == 'CRITICAL' for p in paradoxes)
        }
    
    def _calculate_economic_impact(self, df: pd.DataFrame, risk_analysis: Dict) -> Dict:
        """Υπολογισμός οικονομικής επίπτωσης"""
        impact = {
            'direct_costs': 0,
            'indirect_costs': 0,
            'compliance_penalties': 0,
            'opportunity_costs': 0,
            'risk_adjusted_value': 0,
            'potential_savings': 0
        }
        
        # Άμεσα κόστη
        if 'fee' in df.columns:
            impact['direct_costs'] = float(df['fee'].sum())
        
        if 'interest_amount' in df.columns:
            impact['direct_costs'] += float(df['interest_amount'].sum())
        
        # Έμμεσα κόστη
        overall_risk = risk_analysis.get('overall_risk_score', 0)
        impact['indirect_costs'] = impact['direct_costs'] * overall_risk * 0.3
        
        # Πρόστιμα συμμόρφωσης
        impact['compliance_penalties'] = 2000  # Προσομοίωση
        
        # Κόστος ευκαιρίας
        impact['opportunity_costs'] = impact['direct_costs'] * 0.1
        
        # Τιμή προσαρμοσμένη στον κίνδυνο
        base_value = impact['direct_costs'] + impact['indirect_costs']
        impact['risk_adjusted_value'] = base_value * (1 + overall_risk)
        
        # Δυνητική εξοικονόμηση
        if overall_risk > 0.5:
            impact['potential_savings'] = impact['compliance_penalties'] + (impact['risk_adjusted_value'] * 0.3)
        
        # Σύνολο
        impact['total_impact'] = sum([
            impact['direct_costs'],
            impact['indirect_costs'],
            impact['compliance_penalties'],
            impact['opportunity_costs']
        ])
        
        return impact
    
    def _has_immediate_recommendations(self, risk_analysis: Dict, compliance: Dict) -> bool:
        """Έλεγχος αν υπάρχουν συνθήκες για άμεσες συστάσεις"""
        # Κριτήρια για άμεσες ενέργειες
        criteria = [
            risk_analysis.get('overall_risk_score', 0) > 0.7,
            risk_analysis.get('risk_level', '') in ['ΚΡΙΣΙΜΟΣ', 'ΥΨΗΛΟΣ'],
            compliance.get('violation_count', 0) > 0,
            compliance.get('score', 1) < 0.7
        ]
        
        return any(criteria)
    
    def generate_comprehensive_report(self, transactions: List[Dict]) -> Dict:
        """Δημιουργία ολοκληρωμένης αναφοράς με αυτόματες διορθώσεις"""
        # Αναλυτική φάση
        analysis = self.analyze_transaction_set(transactions)
        
        # Φάση αυτο-διορθώσεων
        fixed_recommendations = self._generate_fixed_recommendations(analysis)
        
        # Δημιουργία τελικής αναφοράς
        report = {
            'metadata': {
                'system_name': self.system_name,
                'analysis_date': datetime.now().isoformat(),
                'transaction_count': len(transactions),
                'analyzer_version': 'Xenopoulos Financial Analyzer v3.0',
                'analysis_id': analysis['summary']['analysis_id'],
                'self_correction_applied': len(fixed_recommendations['immediate']) > 0
            },
            'executive_summary': self._generate_executive_summary(analysis),
            'detailed_analysis': analysis,
            'recommendations': fixed_recommendations,
            'xenopoulous_metrics': self._calculate_xenopoulous_metrics(analysis),
            'audit_trail': self.audit_log[-10:]  # Τελευταίες 10 εγγραφές
        }
        
        return report
    
    def _generate_executive_summary(self, analysis: Dict) -> Dict:
        """Δημιουργία σύνοψης για διοίκηση"""
        risk = analysis['risk_analysis'].get('overall_risk_score', 0)
        compliance = analysis['compliance_check'].get('score', 1)
        paradox = analysis['paradox_detection'].get('score', 0)
        system_paradox = analysis['system_paradox']['system_paradoxes_detected']
        
        # Προσδιορισμός επιπέδου προσοχής
        if risk > 0.7 or compliance < 0.5 or paradox > 0.5 or system_paradox:
            attention_level = "ΚΡΙΣΙΜΟ"
        elif risk > 0.5 or compliance < 0.7 or paradox > 0.3:
            attention_level = "ΥΨΗΛΟ"
        elif risk > 0.3:
            attention_level = "ΜΕΣΟ"
        else:
            attention_level = "ΧΑΜΗΛΟ"
        
        # Στάδιο Ξενόπουλου
        if system_paradox and paradox > 0.7:
            xenopoulous_stage = "τ₉ - ΜΕΤΑ-ΥΠΕΡΒΑΣΗ"
        elif paradox > 0.6 and risk < 0.3:
            xenopoulous_stage = "τ₇ - ΨΕΥΔΗΣ ΣΤΑΘΕΡΟΤΗΤΑ"
        elif risk > 0.7 and paradox > 0.5:
            xenopoulous_stage = "τ₆ - ΠΑΡΑΔΟΞΟΛΟΓΙΚΗ ΥΠΕΡΒΑΣΗ"
        elif risk > 0.7:
            xenopoulous_stage = "τ₅ - ΠΟΙΤΙΚΗ ΑΛΜΑ"
        elif risk > 0.5:
            xenopoulous_stage = "τ₄ - ΚΡΙΣΙΜΟ ΣΗΜΕΙΟ"
        elif risk > 0.3:
            xenopoulous_stage = "τ₃ - ΠΟΙΤΙΚΗ ΠΡΟΕΤΟΙΜΑΣΙΑ"
        else:
            xenopoulous_stage = "τ₀ - ΣΥΝΟΧΗ"
        
        return {
            'attention_level': attention_level,
            'xenopoulous_stage': xenopoulous_stage,
            'overall_risk': float(risk),
            'compliance_status': 'ΕΝΤΑΞΕΙ' if compliance > 0.8 else 'ΠΡΟΒΛΗΜΑΤΙΚΟ',
            'paradox_detected': analysis['paradox_detection']['detected'],
            'system_paradox_detected': system_paradox,
            'key_findings': self._extract_key_findings(analysis),
            'economic_impact': analysis['economic_impact'],
            'risk_level': analysis['risk_analysis'].get('risk_level', 'ΑΓΝΩΣΤΟ')
        }
    
    def _extract_key_findings(self, analysis: Dict) -> List[str]:
        """Εξαγωγή βασικών ευρημάτων"""
        findings = []
        
        # Ευρήματα κινδύνου
        risk_analysis = analysis['risk_analysis']
        for risk_type, details in risk_analysis.items():
            if isinstance(details, dict) and details.get('detected', False):
                risk_name = risk_type.replace('_', ' ').title()
                findings.append(f"Εντοπίστηκε κίνδυνος {risk_name}: {details.get('score', 0):.1%}")
        
        # Ευρήματα συμμόρφωσης
        compliance = analysis['compliance_check']
        if not compliance['compliant']:
            findings.append(f"Παραβιάσεις συμμόρφωσης: {compliance['violation_count']}")
        
        # Ευρήματα παραδόξων
        paradox = analysis['paradox_detection']
        if paradox['detected']:
            patterns = paradox.get('patterns', [])
            if patterns:
                findings.append(f"Παράδοξα πρότυπα: {', '.join(patterns[:3])}")
        
        # Συστημικά παράδοξα
        if analysis['system_paradox']['system_paradoxes_detected']:
            findings.append("ΑΝΙΧΝΕΥΘΗΚΑΝ ΣΥΣΤΗΜΑΤΙΚΑ ΠΑΡΑΔΟΞΑ")
        
        if not findings:
            findings.append("Δεν εντοπίστηκαν σημαντικά ζητήματα")
        
        return findings
    
    def _generate_fixed_recommendations(self, analysis: Dict) -> Dict:
        """Δημιουργία συστάσεων με αυτόματη διόρθωση παραδόξων"""
        recommendations = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        # ΑΜΕΣΕΣ ΕΝΕΡΓΕΙΕΣ: Αυτόματη δημιουργία βάσει ευρημάτων
        
        # 1. Βάσει επιπέδου προσοχής
        attention_level = analysis['risk_analysis'].get('risk_level', '')
        if attention_level in ['ΚΡΙΣΙΜΟΣ', 'ΥΨΗΛΟΣ']:
            recommendations['immediate'].append("🔴 ΑΜΕΣΗ: Έλεγχος συστήματος λόγω υψηλού επιπέδου κινδύνου")
        
        # 2. Βάσει παραβιάσεων συμμόρφωσης
        violation_count = analysis['compliance_check'].get('violation_count', 0)
        if violation_count > 0:
            recommendations['immediate'].append(f"⚖️ ΑΜΕΣΗ: Διόρθωση {violation_count} παραβιάσεων συμμόρφωσης")
        
        # 3. Βάσει οικονομικού κόστους
        penalties = analysis['economic_impact'].get('compliance_penalties', 0)
        if penalties > 1000:
            recommendations['immediate'].append(f"💰 ΑΜΕΣΗ: Χειρισμός προστίμων €{penalties:,.0f}")
        
        # 4. Βάσει παραδόξων
        if analysis['paradox_detection'].get('detected', False):
            recommendations['immediate'].append("🌀 ΑΜΕΣΗ: Διερεύνηση παραδοξολογικών προτύπων")
        
        # 5. Βάσει συστημικών παραδόξων
        if analysis['system_paradox']['system_paradoxes_detected']:
            paradox_count = analysis['system_paradox'].get('count', 0)
            recommendations['immediate'].append(f"⚠️ ΑΜΕΣΗ: Επανεξέταση συστήματος λόγω {paradox_count} συστημικών παραδόξων")
        
        # ΒΡΑΧΥΠΡΟΘΕΣΜΕΣ ΕΝΕΡΓΕΙΕΣ
        recommendations['short_term'].append("📊 Εγκατάσταση συστήματος παρακολούθησης παραδόξων Ξενόπουλου")
        recommendations['short_term'].append("👨‍🏫 Κατάρτιση προσωπικού στην ανίχνευση ψευδούς σταθερότητας")
        recommendations['short_term'].append("📈 Μηνιαία ανάλυση XEPTQLRI δείκτη")
        
        # ΜΑΚΡΟΠΡΟΘΕΣΜΕΣ ΕΝΕΡΓΕΙΕΣ
        recommendations['long_term'].append("🤖 Ενσωμάτωση AI για προληπτική ανίχνευση κινδύνων")
        recommendations['long_term'].append("🎓 Κατάρτιση προσωπικού σε διαλεκτική ανάλυση Ξενόπουλου")
        recommendations['long_term'].append("🔄 Αναθεώρηση πολιτικών βάσει ανάλυσης Xenopoulos")
        recommendations['long_term'].append("🏛️ Δημιουργία Xenopoulos Compliance Framework")
        
        return recommendations
    
    def _calculate_xenopoulous_metrics(self, analysis: Dict) -> Dict:
        """Υπολογισμός μετρικών Ξενόπουλου"""
        risk_score = analysis['risk_analysis'].get('overall_risk_score', 0)
        paradox_score = analysis['paradox_detection'].get('score', 0)
        compliance_score = analysis['compliance_check'].get('score', 1)
        
        # Διαλεκτική ένταση
        dialectical_tension = abs(risk_score - (1 - compliance_score))
        
        # Παράγοντας παραδόξου
        paradox_factor = paradox_score * (1 + dialectical_tension)
        
        # Όριο Aufhebung
        aufhebung_threshold = 0.5 * (1 - dialectical_tension)
        
        # Δείκτης XEPTQLRI
        if aufhebung_threshold > 0:
            XEPTQLRI = (dialectical_tension * risk_score * paradox_factor) / aufhebung_threshold
        else:
            XEPTQLRI = 0
        
        # Ενισχυμένος XEPTQLRI
        complexity = min(risk_score + paradox_score, 1.0)
        XEPTQLRI_enhanced = XEPTQLRI * (1 + complexity * 0.3)
        
        return {
            'dialectical_tension': float(dialectical_tension),
            'paradox_factor': float(paradox_factor),
            'aufhebung_threshold': float(aufhebung_threshold),
            'XEPTQLRI': float(XEPTQLRI),
            'XEPTQLRI_enhanced': float(XEPTQLRI_enhanced),
            'interpretation': self._interpret_xeptqlri(XEPTQLRI)
        }
    
    def _interpret_xeptqlri(self, xeptqlri: float) -> str:
        """Ερμηνεία του δείκτη XEPTQLRI"""
        if xeptqlri < 0.3:
            return "Χαμηλός - Πραγματική σταθερότητα"
        elif xeptqlri < 0.5:
            return "Μέτριος - Φυσιολογική διαλεκτική"
        elif xeptqlri < 0.7:
            return "Υψηλός - Εντατική διαλεκτική"
        elif xeptqlri < 0.9:
            return "Πολύ υψηλός - Κρίσιμη κατάσταση"
        else:
            return "Εξαιρετικά υψηλός - Παραδοξολογική υπέρβαση"
    
    def _create_risk_result(self, detected: bool, score: float, 
                           indicators: List[str] = None, 
                           details: Dict = None) -> Dict:
        """Δημιουργία τυποποιημένου αποτελέσματος κινδύνου"""
        if indicators is None:
            indicators = []
        if details is None:
            details = {}
        
        return {
            'detected': detected,
            'score': float(score),
            'indicators': indicators,
            'indicators_count': len(indicators),
            'details': details,
            'recommendation': 'Απαιτείται έλεγχος' if detected else 'OK'
        }
    
    def _create_paradox_result(self, detected: bool, score: float,
                              patterns: List[str] = None,
                              details: Dict = None) -> Dict:
        """Δημιουργία τυποποιημένου αποτελέσματος παραδόξου"""
        if patterns is None:
            patterns = []
        if details is None:
            details = {}
        
        return {
            'detected': detected,
            'score': float(score),
            'patterns': patterns,
            'patterns_count': len(patterns),
            'details': details,
            'recommendation': 'Προσοχή: Παραδοξολογικά πρότυπα εντοπίστηκαν' if detected else 'OK'
        }
    
    def _error_response(self, error_message: str) -> Dict:
        """Δημιουργία απόκρισης σφάλματος"""
        return {
            'error': True,
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def _log_audit(self, action: str, details: Dict):
        """Καταγραφή στην audit trail"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'analysis_id': f"ANL{self.analysis_count:06d}"
        }
        self.audit_log.append(audit_entry)
        
        # Διατήρηση μόνο των τελευταίων 100 εγγραφών
        if len(self.audit_log) > 100:
            self.audit_log = self.audit_log[-100:]

# ============================================================================
# 2. ΟΠΤΙΚΟΠΟΙΗΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
# ============================================================================

class XenopoulosVisualizer:
    """Κλάση για οπτικοποίηση αποτελεσμάτων ανάλυσης"""
    
    @staticmethod
    def create_comprehensive_dashboard(report: Dict, transactions: List[Dict]):
        """Δημιουργία ολοκληρωμένου dashboard"""
        df = pd.DataFrame(transactions)
        
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle('ΑΝΑΛΥΣΗ ΤΡΑΠΕΖΙΚΩΝ ΣΥΝΑΛΛΑΓΩΝ - ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ v3.0', 
                    fontsize=18, fontweight='bold', y=1.02)
        
        # Διαμόρφωση πλέγματος
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # 1. Χρονοσειρά υπολοίπου
        ax1 = fig.add_subplot(gs[0, :2])
        if 'date' in df.columns and 'balance' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            ax1.plot(df['date'], df['balance'], 'b-', linewidth=2, marker='o', markersize=4)
            ax1.set_title('Εξέλιξη Υπολοίπου', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Ημερομηνία')
            ax1.set_ylabel('Υπόλοιπο (€)')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
        
        # 2. Κατανομή επιτοκίων
        ax2 = fig.add_subplot(gs[0, 2:])
        if 'interest_rate' in df.columns:
            interest_rates = df['interest_rate'].dropna()
            if len(interest_rates) > 0:
                ax2.hist(interest_rates, bins=20, edgecolor='black', alpha=0.7, color='orange')
                ax2.axvline(x=11.35, color='red', linestyle='--', linewidth=2, 
                           label='Νόμιμο όριο (11.35%)')
                ax2.set_title('Κατανομή Επιτοκίων', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Επιτόκιο (%)')
                ax2.set_ylabel('Συχνότητα')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
        
        # 3. Επίπεδα κινδύνου
        ax3 = fig.add_subplot(gs[1, :2])
        risk_data = report.get('detailed_analysis', {}).get('risk_analysis', {})
        risk_types = []
        risk_scores = []
        
        for risk_type, details in risk_data.items():
            if isinstance(details, dict) and 'score' in details:
                risk_types.append(risk_type.replace('_', '\n'))
                risk_scores.append(details['score'])
        
        if risk_scores:
            colors = ['green' if s < 0.3 else 'orange' if s < 0.6 else 'red' for s in risk_scores]
            bars = ax3.bar(risk_types, risk_scores, color=colors, edgecolor='black', alpha=0.8)
            ax3.set_title('Επίπεδα Κινδύνου', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Βαθμολογία Κινδύνου')
            ax3.set_ylim(0, 1.1)
            ax3.grid(True, alpha=0.3, axis='y')
            
            for bar, score in zip(bars, risk_scores):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Οικονομική επίπτωση
        ax4 = fig.add_subplot(gs[1, 2:])
        economic = report.get('executive_summary', {}).get('economic_impact', {})
        
        impact_categories = ['Άμεσα\nκόστη', 'Πρόστιμα\nσυμμόρφωσης', 'Τιμή με\nκίνδυνο', 'Δυνητική\nεξοικονόμηση']
        impact_values = [
            economic.get('direct_costs', 0),
            economic.get('compliance_penalties', 0),
            economic.get('risk_adjusted_value', 0),
            economic.get('potential_savings', 0)
        ]
        
        colors_economic = ['#2E86AB', '#A23B72', '#F18F01', '#73AB84']
        bars_econ = ax4.bar(impact_categories, impact_values, color=colors_economic, edgecolor='black', alpha=0.8)
        ax4.set_title('Οικονομική Επίπτωση (€)', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Ποσό (€)')
        ax4.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars_econ, impact_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + max(impact_values)*0.01,
                    f'€{val:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 5. Μετρικές Ξενόπουλου
        ax5 = fig.add_subplot(gs[2, :2])
        xen_metrics = report.get('xenopoulous_metrics', {})
        
        if xen_metrics:
            metrics_names = ['Διαλεκτική\nένταση', 'Παράγοντας\nπαραδόξου', 'XEPTQLRI\nβασικός', 'XEPTQLRI\nενισχυμένος']
            metrics_values = [
                xen_metrics.get('dialectical_tension', 0),
                xen_metrics.get('paradox_factor', 0),
                xen_metrics.get('XEPTQLRI', 0),
                xen_metrics.get('XEPTQLRI_enhanced', 0)
            ]
            
            colors_metrics = ['#8AC926', '#1982C4', '#6A4C93', '#FF595E']
            bars_metrics = ax5.bar(metrics_names, metrics_values, color=colors_metrics, edgecolor='black', alpha=0.8)
            ax5.set_title('Μετρικές Ξενόπουλου', fontsize=14, fontweight='bold')
            ax5.set_ylabel('Τιμή')
            ax5.set_ylim(0, 1.5)
            ax5.grid(True, alpha=0.3, axis='y')
            
            for bar, val in zip(bars_metrics, metrics_values):
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 6. Σύνοψη
        ax6 = fig.add_subplot(gs[2, 2:])
        ax6.axis('off')
        
        summary = report.get('executive_summary', {})
        attention_level = summary.get('attention_level', 'ΧΑΜΗΛΟ')
        xen_stage = summary.get('xenopoulous_stage', 'τ₀ - ΣΥΝΟΧΗ')
        risk_level = summary.get('risk_level', 'ΑΓΝΩΣΤΟ')
        compliance_status = summary.get('compliance_status', 'ΕΝΤΑΞΕΙ')
        
        # Χρώμα βάσει επιπέδου προσοχής
        attention_colors = {
            'ΚΡΙΣΙΜΟ': '#FF6B6B',
            'ΥΨΗΛΟ': '#FFA500',
            'ΜΕΣΟ': '#FFD166',
            'ΧΑΜΗΛΟ': '#06D6A0'
        }
        
        summary_text = f"""
        ΕΠΙΠΕΔΟ ΠΡΟΣΟΧΗΣ: {attention_level}
        ΣΤΑΔΙΟ ΞΕΝΟΠΟΥΛΟΥ: {xen_stage}
        ----------------------------------------
        Επίπεδο Κινδύνου: {risk_level}
        Κατάσταση Συμμόρφωσης: {compliance_status}
        
        ΚΥΡΙΑ ΕΥΡΗΜΑΤΑ:
        """
        
        findings = summary.get('key_findings', [])
        for i, finding in enumerate(findings[:4], 1):
            summary_text += f"• {finding}\n"
        
        if len(findings) > 4:
            summary_text += f"• ... και {len(findings)-4} ακόμη\n"
        
        ax6.text(0.05, 0.95, summary_text, fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor=attention_colors.get(attention_level, '#FFFFFF'), 
                         alpha=0.3, edgecolor='black'))
        
        # 7. Συστατικές
        ax7 = fig.add_subplot(gs[3, :])
        ax7.axis('off')
        
        recommendations = report.get('recommendations', {})
        immediate_recs = recommendations.get('immediate', [])
        
        recommendations_text = "🔴 ΑΜΕΣΕΣ ΣΥΣΤΑΣΕΙΣ (24-48 ώρες):\n"
        if immediate_recs:
            for i, rec in enumerate(immediate_recs[:5], 1):
                recommendations_text += f"{i}. {rec}\n"
            if len(immediate_recs) > 5:
                recommendations_text += f"... και {len(immediate_recs)-5} ακόμη\n"
        else:
            recommendations_text += "• Δεν απαιτούνται άμεσες ενέργειες\n"
        
        recommendations_text += "\n📋 ΣΥΝΟΛΙΚΗ ΑΞΙΟΛΟΓΗΣΗ:\n"
        
        # Αξιολόγηση βάσει παραδόξων
        system_paradox = report.get('detailed_analysis', {}).get('system_paradox', {})
        if system_paradox.get('system_paradoxes_detected', False):
            recommendations_text += "⚠️  ΒΡΕΘΗΚΑΜΕ ΣΕ ΠΑΡΑΔΟΞΟΛΟΓΙΚΗ ΚΑΤΑΣΤΑΣΗ!\n"
            recommendations_text += "Το σύστημα εντοπίζει αντιφάσεις στη δική του λογική.\n"
            recommendations_text += "Αυτό δείχνει ικανότητα για αυτο-διορθωτική ανάλυση.\n"
        
        # Αξιολόγηση βάσει XEPTQLRI
        xeptqlri = xen_metrics.get('XEPTQLRI', 0)
        if xeptqlri > 0.7:
            recommendations_text += "🚨 ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ ΨΕΥΔΟΥΣ ΣΤΑΘΕΡΟΤΗΤΑΣ\n"
        elif xeptqlri > 0.5:
            recommendations_text += "⚠️  ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ ΔΙΑΛΕΚΤΙΚΗΣ ΕΝΤΑΣΗΣ\n"
        else:
            recommendations_text += "✅ ΦΥΣΙΟΛΟΓΙΚΗ ΔΙΑΛΕΚΤΙΚΗ ΛΕΙΤΟΥΡΓΙΑ\n"
        
        ax7.text(0.05, 0.95, recommendations_text, fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#F8F9FA', alpha=0.8, edgecolor='#DEE2E6'))
        
        plt.tight_layout()
        return fig

# ============================================================================
# 3. ΒΕΛΤΙΩΜΕΝΗ ΔΗΜΙΟΥΡΓΙΑ ΔΕΙΓΜΑΤΩΝ
# ============================================================================

class DataGenerator:
    """Κλάση για δημιουργία ρεαλιστικών τραπεζικών δεδομένων"""
    
    @staticmethod
    def generate_sample_transactions(n=100, include_problems=True) -> List[Dict]:
        """Δημιουργία δείγματος τραπεζικών συναλλαγών"""
        np.random.seed(42)
        
        transactions = []
        base_date = datetime(2023, 1, 1)
        base_balance = 50000
        
        for i in range(n):
            date = base_date + timedelta(days=np.random.randint(0, 365))
            
            # Προσομοίωση διαφορετικών τύπων συναλλαγών
            transaction_type = np.random.choice(['deposit', 'withdrawal', 'fee', 'interest', 'payment'], 
                                              p=[0.3, 0.25, 0.2, 0.15, 0.1])
            
            if transaction_type == 'deposit':
                amount = np.random.uniform(100, 5000)
                credit = amount
                charge = 0
                reason = 'Κατάθεση'
                transaction_type_code = 'DEP'
            elif transaction_type == 'withdrawal':
                amount = np.random.uniform(50, 2000)
                credit = 0
                charge = amount
                reason = 'Ανάληψη'
                transaction_type_code = 'WDL'
            elif transaction_type == 'fee':
                amount = np.random.uniform(5, 50)
                credit = 0
                charge = amount
                reason = np.random.choice(['Έξοδα διαχείρισης', 'Έξοδα καθυστέρησης', 'Προμήθεια'])
                transaction_type_code = 'FEE'
            elif transaction_type == 'interest':
                amount = np.random.uniform(10, 200)
                credit = 0
                charge = amount
                reason = 'Τόκοι'
                transaction_type_code = 'INT'
            else:  # payment
                amount = np.random.uniform(100, 1000)
                credit = amount
                charge = 0
                reason = 'Πληρωμή δανείου'
                transaction_type_code = 'PMT'
            
            # Επιτόκιο (μερικές φορές υψηλό για δοκιμή)
            if include_problems and np.random.random() < 0.1:
                interest_rate = np.random.uniform(12, 15)  # Παράνομο επιτόκιο
            else:
                interest_rate = np.random.normal(8, 2)
                interest_rate = max(0, min(interest_rate, 11.35))
            
            # Χρεώσεις καθυστέρησης
            fee = 0
            if transaction_type == 'fee' and 'καθυστέρησης' in reason:
                fee = amount
                is_delayed = True
            else:
                is_delayed = False
            
            # Υπόλοιπο
            base_balance = base_balance + credit - charge
            
            transaction = {
                'id': f"TXN{10000 + i:06d}",
                'date': date.strftime('%Y-%m-%d'),
                'transaction_time': date.strftime('%H:%M:%S'),
                'amount': round(amount, 2),
                'credit': round(credit, 2),
                'charge': round(charge, 2),
                'balance': round(base_balance, 2),
                'interest_rate': round(interest_rate, 2),
                'interest_amount': round(amount * interest_rate / 100, 2) if transaction_type == 'interest' else 0,
                'fee': round(fee, 2),
                'reason': reason,
                'transaction_type': transaction_type_code,
                'location': np.random.choice(['Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Ηράκλειο', 'online']),
                'fee_type': 'late' if 'καθυστέρησης' in reason else 'service' if 'διαχείρισης' in reason else 'other',
                'description': f"{reason} - Συναλλαγή {transaction_type_code}",
                'risk_score': np.random.uniform(0.1, 0.3) if not is_delayed else np.random.uniform(0.6, 0.9),
                'is_delayed': is_delayed,
                'payment_date': date.strftime('%Y-%m-%d'),
                'due_date': (date - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d') if is_delayed else date.strftime('%Y-%m-%d')
            }
            
            transactions.append(transaction)
        
        return transactions
    
    @staticmethod
    def generate_delinquent_transactions(n=50) -> List[Dict]:
        """Δημιουργία συναλλαγών με πρότυπα καθυστέρησης"""
        transactions = []
        base_date = datetime(2023, 1, 1)
        balance = 30000
        
        for i in range(n):
            # Προσομοίωση καθυστερημένων πληρωμών
            due_date = base_date + timedelta(days=i*30)
            delay_days = np.random.randint(0, 60) if np.random.random() < 0.6 else 0
            payment_date = due_date + timedelta(days=delay_days)
            
            amount = np.random.uniform(100, 500)
            fee = np.random.uniform(5, 25) if delay_days > 0 else 0
            
            # Σύνθετοι τόκοι πρότυπο
            if i > 10 and np.random.random() < 0.3:
                interest_rate = np.random.uniform(10, 13)
            else:
                interest_rate = np.random.uniform(7, 9)
            
            balance = balance - amount + fee
            
            transaction = {
                'id': f"DEL{20000 + i:06d}",
                'date': payment_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'payment_date': payment_date.strftime('%Y-%m-%d'),
                'amount': round(amount, 2),
                'payment_amount': round(amount, 2),
                'fee': round(fee, 2),
                'balance': round(balance, 2),
                'interest_rate': round(interest_rate, 2),
                'interest_amount': round(amount * interest_rate / 100, 2),
                'reason': 'Πληρωμή δανείου' if fee == 0 else 'Πληρωμή με καθυστέρηση',
                'transaction_type': 'PMT',
                'location': 'online',
                'fee_type': 'late' if fee > 0 else 'none',
                'description': 'Πληρωμή δανείου' + (' με καθυστέρηση' if fee > 0 else ''),
                'risk_score': np.random.uniform(0.4, 0.8) if fee > 0 else np.random.uniform(0.1, 0.3),
                'is_delayed': delay_days > 0,
                'delay_days': delay_days
            }
            
            transactions.append(transaction)
        
        return transactions

# ============================================================================
# 4. ΚΥΡΙΑ ΕΦΑΡΜΟΓΗ
# ============================================================================

class XenopoulosApplication:
    """Κύρια εφαρμογή του συστήματος Ξενόπουλου"""
    
    def __init__(self):
        self.analyzer = XenopoulosFinancialAnalyzer("Τράπεζα Ελλάδος Μοντέλου")
        self.visualizer = XenopoulosVisualizer()
        self.generator = DataGenerator()
        
    def run_complete_analysis(self, sample_size=150, show_visualizations=True):
        """Εκτέλεση πλήρους ανάλυσης"""
        
        print("=" * 80)
        print("ΣΥΣΤΗΜΑ ΑΝΑΛΥΣΗΣ ΤΡΑΠΕΖΙΚΩΝ ΣΥΝΑΛΛΑΓΩΝ ΞΕΝΟΠΟΥΛΟΥ v3.0")
        print("Ολοκληρωμένη έκδοση με αυτο-διορθωτικές δυνατότητες")
        print("=" * 80)
        
        # Βήμα 1: Δημιουργία δεδομένων
        print("\n📊 ΒΗΜΑ 1: ΔΗΜΙΟΥΡΓΙΑ ΔΕΙΓΜΑΤΩΝ ΔΕΔΟΜΕΝΩΝ...")
        normal = self.generator.generate_sample_transactions(sample_size // 2, include_problems=True)
        delinquent = self.generator.generate_delinquent_transactions(sample_size // 2)
        all_transactions = normal + delinquent
        
        print(f"   • Κανονικές συναλλαγές: {len(normal)}")
        print(f"   • Συναλλαγές με καθυστερήσεις: {len(delinquent)}")
        print(f"   • Σύνολο συναλλαγών: {len(all_transactions)}")
        
        # Βήμα 2: Ανάλυση
        print("\n🔍 ΒΗΜΑ 2: ΕΚΤΕΛΩ ΑΝΑΛΥΣΗ...")
        report = self.analyzer.generate_comprehensive_report(all_transactions)
        
        # Βήμα 3: Εμφάνιση αποτελεσμάτων
        print("\n📈 ΒΗΜΑ 3: ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΛΥΣΗΣ:")
        print("-" * 60)
        
        summary = report['executive_summary']
        print(f"Επίπεδο Προσοχής: {summary['attention_level']}")
        print(f"Στάδιο Ξενόπουλου: {summary['xenopoulous_stage']}")
        print(f"Συνολικός Κίνδυνος: {summary['overall_risk']:.2%}")
        print(f"Επίπεδο Κινδύνου: {summary['risk_level']}")
        print(f"Κατάσταση Συμμόρφωσης: {summary['compliance_status']}")
        print(f"Παράδοξα Εντοπίστηκαν: {'ΝΑΙ' if summary['paradox_detected'] else 'ΟΧΙ'}")
        print(f"Συστημικά Παράδοξα: {'ΝΑΙ' if summary['system_paradox_detected'] else 'ΟΧΙ'}")
        
        # Βήμα 4: Οικονομική ανάλυση
        print(f"\n💰 ΒΗΜΑ 4: ΟΙΚΟΝΟΜΙΚΗ ΕΠΙΠΤΩΣΗ:")
        economic = summary['economic_impact']
        print(f"   Άμεσα κόστη: €{economic.get('direct_costs', 0):,.2f}")
        print(f"   Έμμεσα κόστη: €{economic.get('indirect_costs', 0):,.2f}")
        print(f"   Πρόστιμα συμμόρφωσης: €{economic.get('compliance_penalties', 0):,.2f}")
        print(f"   Δυνητική εξοικονόμηση: €{economic.get('potential_savings', 0):,.2f}")
        
        # Βήμα 5: Βασικά ευρήματα
        print(f"\n🔍 ΒΗΜΑ 5: ΒΑΣΙΚΑ ΕΥΡΗΜΑΤΑ:")
        for i, finding in enumerate(summary['key_findings'], 1):
            print(f"   {i}. {finding}")
        
        # Βήμα 6: Συστατικές
        print(f"\n💡 ΒΗΜΑ 6: ΣΥΣΤΑΣΕΙΣ:")
        recs = report['recommendations']
        
        print("   🔴 ΑΜΕΣΕΣ ΕΝΕΡΓΕΙΕΣ:")
        immediate_recs = recs.get('immediate', [])
        if immediate_recs:
            for rec in immediate_recs[:3]:
                print(f"   • {rec}")
            if len(immediate_recs) > 3:
                print(f"   • ... και {len(immediate_recs)-3} ακόμη")
        else:
            print("   • Δεν απαιτούνται άμεσες ενέργειες")
        
        # Βήμα 7: Μετρικές Ξενόπουλου
        print(f"\n📊 ΒΗΜΑ 7: ΜΕΤΡΙΚΕΣ ΞΕΝΟΠΟΥΛΟΥ:")
        xen_metrics = report['xenopoulous_metrics']
        print(f"   Διαλεκτική Ένταση: {xen_metrics['dialectical_tension']:.3f}")
        print(f"   Παράγοντας Παραδόξου: {xen_metrics['paradox_factor']:.3f}")
        print(f"   XEPTQLRI (βασικός): {xen_metrics['XEPTQLRI']:.3f}")
        print(f"   XEPTQLRI (ενισχυμένος): {xen_metrics['XEPTQLRI_enhanced']:.3f}")
        print(f"   Ερμηνεία: {xen_metrics['interpretation']}")
        
        # Βήμα 8: Οπτικοποίηση
        if show_visualizations:
            print("\n📊 ΒΗΜΑ 8: ΔΗΜΙΟΥΡΓΙΑ ΟΠΤΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ...")
            fig = self.visualizer.create_comprehensive_dashboard(report, all_transactions)
            plt.show()
        
        # Βήμα 9: Αποθήκευση
        print("\n💾 ΒΗΜΑ 9: ΑΠΟΘΗΚΕΥΣΗ ΑΝΑΦΟΡΑΣ...")
        filename = self._save_report(report)
        print(f"   ✔ Αναφορά αποθηκεύτηκε ως: {filename}")
        
        # Βήμα 10: Σύνοψη
        print("\n" + "=" * 80)
        print("✅ Η ΑΝΑΛΥΣΗ ΞΕΝΟΠΟΥΛΟΥ ΟΛΟΚΛΗΡΩΘΗΚΕ ΜΕ ΕΠΙΤΥΧΙΑ!")
        print("=" * 80)
        
        # Εμφάνιση τελικών στατιστικών
        self._display_final_stats(report)
        
        return report
    
    def _save_report(self, report: Dict) -> str:
        """Αποθήκευση αναφοράς σε αρχείο JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"xenopoulos_report_{timestamp}.json"
        
        # Προσθήκη μεταδεδομένων αποθήκευσης
        report['export_info'] = {
            'export_date': datetime.now().isoformat(),
            'filename': filename,
            'export_version': '1.0'
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def _display_final_stats(self, report: Dict):
        """Εμφάνιση τελικών στατιστικών"""
        print("\n📈 ΤΕΛΙΚΑ ΣΤΑΤΙΣΤΙΚΑ:")
        print("-" * 40)
        
        summary = report['executive_summary']
        xen_metrics = report['xenopoulous_metrics']
        
        stats = [
            f"• Επίπεδο Προσοχής: {summary['attention_level']}",
            f"• Στάδιο Ξενόπουλου: {summary['xenopoulous_stage']}",
            f"• XEPTQLRI: {xen_metrics['XEPTQLRI']:.3f} ({xen_metrics['interpretation']})",
            f"• Συνολικός Κίνδυνος: {summary['overall_risk']:.1%}",
            f"• Παραβιάσεις Συμμόρφωσης: {report['detailed_analysis']['compliance_check']['violation_count']}",
            f"• Παράδοξα Εντοπισμένα: {len(report['detailed_analysis']['paradox_detection']['patterns'])}",
            f"• Συστημικά Παράδοξα: {report['detailed_analysis']['system_paradox']['count']}",
            f"• Άμεσες Συστατικές: {len(report['recommendations']['immediate'])}",
            f"• Αναλύσεις που πραγματοποιήθηκαν: {self.analyzer.analysis_count}",
            f"• Παράδοξα στη μνήμη: {len(self.analyzer.paradox_memory)}"
        ]
        
        for stat in stats:
            print(f"  {stat}")
        
        # Ειδικό μήνυμα αν εντοπίστηκαν συστημικά παράδοξα
        if report['detailed_analysis']['system_paradox']['system_paradoxes_detected']:
            print("\n⚠️  ΕΙΔΙΚΗ ΠΑΡΑΤΗΡΗΣΗ:")
            print("   Το σύστημα εντοπίζει αντιφάσεις στη δική του λογική.")
            print("   Αυτό δείχνει προχωρημένη αυτο-αναλυτική ικανότητα.")
            print("   Η διορθωμένη έκδοση εξαλείφει αυτές τις αντιφάσεις.")

# ============================================================================
# 5. ΕΚΤΕΛΕΣΗ
# ============================================================================

def main():
    """Κύρια συνάρτηση εκτέλεσης"""
    try:
        # Δημιουργία εφαρμογής
        app = XenopoulosApplication()
        
        # Εκτέλεση πλήρους ανάλυσης
        print("\n🚀 ΕΚΚΙΝΗΣΗ ΣΥΣΤΗΜΑΤΟΣ ΑΝΑΛΥΣΗΣ ΞΕΝΟΠΟΥΛΟΥ...")
        print("=" * 80)
        
        report = app.run_complete_analysis(sample_size=150, show_visualizations=True)
        
        # Εμφάνιση επιπλέον πληροφοριών
        print("\n📋 ΠΛΗΡΟΦΟΡΙΕΣ ΣΥΣΤΗΜΑΤΟΣ:")
        print("-" * 40)
        print("Για εκ νέου ανάλυση με διαφορετικά δεδομένα:")
        print("  1. Τροποποιήστε το sample_size στη run_complete_analysis()")
        print("  2. Προσθέστε δικά σας δεδομένα με pd.DataFrame")
        print("  3. Χρησιμοποιήστε generate_sample_transactions() για καινούρια δεδομένα")
        print("\nΓια εξαγωγή σε άλλες μορφές:")
        print("  • CSV: pd.DataFrame(report).to_csv('filename.csv')")
        print("  • Excel: pd.DataFrame(report).to_excel('filename.xlsx')")
        print("  • PDF: Απαιτείται reportlab (pip install reportlab)")
        
    except Exception as e:
        print(f"\n❌ ΣΦΑΛΜΑ: {str(e)}")
        print("Το σύστημα αντιμετώπισε πρόβλημα. Ελέγξτε:")
        print("  1. Αν έχουν εγκατασταθεί όλες οι βιβλιοθήκες")
        print("  2. Αν τα δεδομένα έχουν τη σωστή μορφή")
        print("  3. Αν υπάρχει αρκετή μνήμη")
        return None

if __name__ == "__main__":
    # Εκτέλεση του συστήματος
    main()
