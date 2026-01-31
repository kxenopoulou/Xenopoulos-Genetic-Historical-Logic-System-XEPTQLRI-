# Αυτό ακριβώς μπες στον financial_analysis.py
# Χρηματοοικονομική ανάλυση με Σύστημα Ξενόπουλου

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class XenopoulosFinancialAnalyzer:
    """Χρηματοοικονομική ανάλυση με διαλεκτική λογική"""
    
    def __init__(self, initial_confidence=0.5):
        self.market_confidence = initial_confidence  # A
        self.risk_perception = -initial_confidence * 0.8  # ¬A
        self.history = []
        self.paradox_alerts = []
        
    def update_market_state(self, price_change, volume, volatility):
        """Ενημέρωση κατάστασης αγοράς"""
        # Κανονικοποίηση παραμέτρων
        norm_change = np.tanh(price_change / 0.1)  # ±10% → ±1
        norm_volume = np.tanh((volume - 1e6) / 5e5)  # Ροή συναλλαγών
        norm_vol = np.tanh(volatility / 0.05)  # Διακύμανση
        
        # Διαλεκτική ενημέρωση
        confidence_change = 0.7 * norm_change + 0.2 * norm_volume - 0.1 * norm_vol
        risk_change = -0.6 * norm_change + 0.3 * norm_vol - 0.1 * norm_volume
        
        self.market_confidence = np.tanh(self.market_confidence + confidence_change)
        self.risk_perception = np.tanh(self.risk_perception + risk_change)
        
        # Υπολογισμός XEPTQLRI
        tension = abs(self.market_confidence * self.risk_perception)
        paradox_factor = self._calculate_paradox_factor()
        xeptqlri = (tension * (1 + abs(confidence_change)) * paradox_factor) / 0.65
        
        # Καταγραφή
        state = {
            'date': datetime.now(),
            'confidence': self.market_confidence,
            'risk': self.risk_perception,
            'tension': tension,
            'xeptqlri': xeptqlri,
            'price_change': price_change,
            'volume': volume,
            'volatility': volatility
        }
        
        self.history.append(state)
        
        # Έλεγχος για παραδοξολογική υπέρβαση
        if self._detect_paradoxical_transcendence():
            alert = {
                'date': state['date'],
                'confidence': self.market_confidence,
                'risk': self.risk_perception,
                'xeptqlri': xeptqlri,
                'message': "ΠΑΡΑΔΟΞΟΛΟΓΙΚΗ ΥΠΕΡΒΑΣΗ: Υψηλή εμπιστοσύνη και υψηλός κίνδυνος ταυτόχρονα"
            }
            self.paradox_alerts.append(alert)
            print(f"⚠️ ΧΡΗΜΑΤΟΟΙΚΟΝΟΜΙΚΗ ΕΙΔΟΠΟΙΗΣΗ: {alert['message']}")
        
        return state
    
    def _calculate_paradox_factor(self):
        """Υπολογισμός παραγόντα παραδόξου για χρηματοοικονομικά δεδομένα"""
        if len(self.history) < 5:
            return 0.5
        
        recent = self.history[-5:]
        extreme_confidence = sum(1 for s in recent if abs(s['confidence']) > 0.8) / 5
        extreme_risk = sum(1 for s in recent if abs(s['risk']) > 0.8) / 5
        
        # Παράγοντας παραδόξου: και τα δύο ακραία ταυτόχρονα
        return extreme_confidence * extreme_risk * 1.5
    
    def _detect_paradoxical_transcendence(self):
        """Ανίχνευση παραδοξολογικής υπέρβασης στις χρηματοοικονομικές αγορές"""
        # Κριτήρια Ξενόπουλου για χρηματοοικονομικά συστήματα
        simultaneous_extremity = (abs(self.market_confidence) > 0.85 and 
                                 abs(self.risk_perception) > 0.85)
        low_tension = abs(self.market_confidence * self.risk_perception) < 0.25
        
        return simultaneous_extremity and low_tension
    
    def analyze_crisis_period(self, start_date, end_date, price_data):
        """Ανάλυση κρίσιμης περιόδου"""
        print(f"\n🔍 ΑΝΑΛΥΣΗ ΚΡΙΣΙΜΗΣ ΠΕΡΙΟΔΟΥ: {start_date} έως {end_date}")
        
        crisis_indicators = {
            'paradox_count': 0,
            'max_xeptqlri': 0,
            'confidence_range': (0, 0),
            'risk_range': (0, 0)
        }
        
        # Προσομοίωση δεδομένων κρίσης
        for date, price in price_data.items():
            # Υπολογισμός αλλαγών
            if len(self.history) > 0:
                prev_price = self.history[-1].get('price', price)
                change = (price - prev_price) / prev_price
                volume = np.random.uniform(5e5, 2e6)
                volatility = np.random.uniform(0.02, 0.1)
            else:
                change = 0
                volume = 1e6
                volatility = 0.05
            
            state = self.update_market_state(change, volume, volatility)
            
            if state['xeptqlri'] > crisis_indicators['max_xeptqlri']:
                crisis_indicators['max_xeptqlri'] = state['xeptqlri']
            
            if self._detect_paradoxical_transcendence():
                crisis_indicators['paradox_count'] += 1
        
        return crisis_indicators
    
    def generate_financial_report(self):
        """Δημιουργία χρηματοοικονομικής αναφοράς"""
        if not self.history:
            return "Δεν υπάρχουν δεδομένα για ανάλυση"
        
        df = pd.DataFrame(self.history)
        
        report = f"""
        📊 ΧΡΗΜΑΤΟΟΙΚΟΝΟΜΙΚΗ ΑΝΑΛΥΣΗ ΞΕΝΟΠΟΥΛΟΥ
        {'='*50}
        
        Στατιστικά Στοιχεία:
        • Περίοδος ανάλυσης: {len(self.history)} ημέρες
        • Παραδοξολογικές ειδοποιήσεις: {len(self.paradox_alerts)}
        • Μέση εμπιστοσύνη αγοράς: {df['confidence'].mean():.3f}
        • Μέση αντίληψη κινδύνου: {df['risk'].mean():.3f}
        • Μέγιστος XEPTQLRI: {df['xeptqlri'].max():.3f}
        
        Κίνδυνοι που εντοπίστηκαν:
        """
        
        if len(self.paradox_alerts) > 0:
            report += f"\n⚠️  ΕΝΤΟΠΙΣΘΗΚΑΝ {len(self.paradox_alerts)} ΠΕΡΙΠΤΩΣΕΙΣ ΠΑΡΑΔΟΞΟΥ:\n"
            for alert in self.paradox_alerts[-3:]:  # Τελευταίες 3
                report += f"   - {alert['date'].strftime('%Y-%m-%d')}: XEPTQLRI={alert['xeptqlri']:.3f}\n"
        
        # Συμβουλές
        if df['xeptqlri'].mean() > 0.7:
            report += "\n🔴 ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ: Προτείνεται μείωση έκθεσης"
        elif df['xeptqlri'].mean() > 0.4:
            report += "\n🟡 ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ: Παρακολούθηση εντατικά"
        else:
            report += "\n🟢 ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ: Κανονική λειτουργία"
        
        return report

# ΠΑΡΑΔΕΙΓΜΑ ΧΡΗΣΗΣ
if __name__ == "__main__":
    print("🧠 ΣΥΣΤΗΜΑ ΧΡΗΜΑΤΟΟΙΚΟΝΟΜΙΚΗΣ ΑΝΑΛΥΣΗΣ ΞΕΝΟΠΟΥΛΟΥ")
    print("="*60)
    
    # Δημιουργία αναλυτή
    analyzer = XenopoulosFinancialAnalyzer(initial_confidence=0.6)
    
    # Προσομοίωση δεδομένων (252 ημέρες συναλλαγών = 1 έτος)
    dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
    prices = np.cumprod(1 + np.random.normal(0.001, 0.02, 252)) * 100
    
    price_data = {date: price for date, price in zip(dates, prices)}
    
    # Ανάλυση
    crisis_results = analyzer.analyze_crisis_period(
        start_date='2023-01-01',
        end_date='2023-12-31',
        price_data=price_data
    )
    
    # Αναφορά
    report = analyzer.generate_financial_report()
    print(report)
    
    print(f"\n📈 ΑΠΟΤΕΛΕΣΜΑΤΑ ΚΡΙΣΗΣ:")
    print(f"   • Παραδοξολογικά γεγονότα: {crisis_results['paradox_count']}")
    print(f"   • Μέγιστος XEPTQLRI: {crisis_results['max_xeptqlri']:.3f}")
    
    print("\n✅ Η ΧΡΗΜΑΤΟΟΙΚΟΝΟΜΙΚΗ ΑΝΑΛΥΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ!")
