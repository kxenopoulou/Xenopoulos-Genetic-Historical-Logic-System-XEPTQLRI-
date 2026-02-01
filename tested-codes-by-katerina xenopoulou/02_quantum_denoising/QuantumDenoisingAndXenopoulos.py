# ============================================
# ΕΓΚΑΤΑΣΤΑΣΗ & ΡΥΘΜΙΣΕΙΣ
# ============================================
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Rescaling
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import warnings
import ipywidgets as widgets
from IPython.display import display, clear_output
import seaborn as sns

warnings.filterwarnings('ignore')

# Ρυθμίσεις οπτικοποίησης
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
print("✅ Βιβλιοθήκες φορτώθηκαν!")

# ============================================
# ΠΥΡΗΝΑΣ ΣΥΣΤΗΜΑΤΟΣ ΞΕΝΟΠΟΥΛΟΥ
# ============================================

class XenopoulosSystem:
    """Βελτιωμένη έκδοση του Γενετικο-Ιστορικού Συστήματος Λογικής"""

    def __init__(self, initial_state_A=0.3, historical_horizon=200,
                 aufhebung_threshold=0.85, system_name="Xenopoulos_LSTM_Analysis"):
        self.A = np.clip(initial_state_A, -1.5, 1.5)
        self.horizon = historical_horizon
        self.aufhebung_threshold = aufhebung_threshold
        self.system_name = system_name

        # Ιστορικά δεδομένα
        self.history_A = []
        self.history_anti_A = []
        self.history_tension = []
        self.history_XEPTQLRI = []
        self.history_stages = []
        self.history_stage_names = []
        self.risk_events = []
        self.paradox_events = []

        # Βελτιωμένοι ορισμοί σταδίων
        self.stages = {
            0: ("τ₀: Coherence", "#2E8B57", "✅"),
            1: ("τ₁: First Anomaly", "#3CB371", "⚠️"),
            2: ("τ₂: Anomaly Repetition", "#FFD700", "🔄"),
            3: ("τ₃: Meaning Incompatibility", "#FFA500", "⚡"),
            4: ("τ₄: System Saturation", "#FF6347", "🔥"),
            5: ("τ₅: Qualitative Leap (⤊)", "#DC143C", "⤊"),
            6: ("τ₆: Paradoxical Transcendence (⟡)", "#8A2BE2", "⟡"),
            7: ("τ₇: False Stability", "#FF69B4", "🎭"),
            8: ("τ₈: Permanent Dialectics", "#A9A9A9", "∞"),
            9: ("τ₉: Meta-Transcendence", "#000000", "🌀")
        }

        print(f"📊 Σύστημα Ξενόπουλου: '{system_name}'")
        print(f"   Αρχική κατάσταση: A = {self.A:.3f}")
        print(f"   Όρια ανίχνευσης: {len(self.stages)} στάδια")

    def _dialectical_negation(self, state):
        """Βελτιωμένος τελεστής ¬ᴰ με μνήμη και τυχαιότητα"""
        # Μνήμη από τα τελευταία 10 βήματα
        memory_effect = 0.0
        if len(self.history_A) > 0:
            window = min(10, len(self.history_A))
            recent_mean = np.mean(self.history_A[-window:])
            memory_effect = 0.2 * np.tanh(recent_mean * 2)

        # Παράγοντας διατήρησης (Xenopoulos: διατηρεί το Α)
        preservation = 0.7 + 0.3 * np.random.rand()

        # Βάρος ιστορικής τάσης
        historical_weight = 1.0 + 0.3 * np.random.rand()

        # Υπολογισμός άρνησης
        negation = -state * preservation * historical_weight * (1 + memory_effect)

        # Στοχαστική συνιστώσα με προσαρμοστικό πλάτος
        noise_level = 0.05 * (1 + abs(state))
        stochastic = noise_level * np.random.randn()

        return np.clip(negation + stochastic, -1.5, 1.5)

    def _calculate_tension(self, state, anti_state):
        """Διαλεκτική ένταση με μη-γραμμική κλιμάκωση"""
        raw_intensity = np.abs(state * anti_state)

        # Ενίσχυση για ακραίες τιμές
        if abs(state) > 0.8 and abs(anti_state) > 0.8:
            intensity = raw_intensity ** 0.7 * 1.5
        elif abs(state) > 0.6 or abs(anti_state) > 0.6:
            intensity = raw_intensity ** 0.8 * 1.2
        else:
            intensity = raw_intensity

        return np.clip(intensity, 0, 1)

    def _calculate_XEPTQLRI(self, tension, current_A, current_anti_A):
        """Βελτιωμένος υπολογισμός XEPTQLRI"""
        # 1. Βάση από ένταση (υπερβολική για μεγάλες τιμές)
        base_risk = tension ** 1.2

        # 2. Ιστορική τάση (τελευταία 5 βήματα)
        trend_factor = 1.0
        if len(self.history_tension) >= 5:
            recent_tension = self.history_tension[-5:]
            trend = np.polyfit(range(5), recent_tension, 1)[0]
            trend_factor = 1.0 + abs(trend) * 15

        # 3. Παράγοντας παραδόξου (ΚΡΙΤΙΚΟ)
        paradox_factor = 1.0
        if abs(current_A) > 0.8 and abs(current_anti_A) > 0.8:
            if tension < 0.35:  # Χαμηλή ένταση + ακραίες τιμές
                paradox_factor = 2.8
            else:
                paradox_factor = 2.0
        elif abs(current_A) > 0.9 or abs(current_anti_A) > 0.9:
            paradox_factor = 1.5

        # 4. Παράγοντας ασυμμετρίας
        asymmetry = abs(abs(current_A) - abs(current_anti_A))
        asymmetry_factor = 1.0 + (1 - asymmetry) * 0.5

        # 5. Τελικός υπολογισμός
        XEPTQLRI = (base_risk * trend_factor * paradox_factor * asymmetry_factor) / self.aufhebung_threshold

        # Τελική προσαρμογή με ομαλοποίηση
        final_XEPTQLRI = XEPTQLRI * (0.9 + 0.2 * np.random.rand())

        return np.clip(final_XEPTQLRI, 0, 3.5)

    def _classify_stage(self, tension, current_A, current_anti_A):
        """Βελτιωμένη ταξινόμηση με πολλαπλά κριτήρια"""
        stage_info = self.stages

        # ΚΡΙΤΗΡΙΟ 1: Παραδοξογενής Υπέρβαση (προτεραιότητα)
        if abs(current_A) > 0.85 and abs(current_anti_A) > 0.85:
            if tension < 0.4:
                return 6, stage_info[6]

        # ΚΡΙΤΗΡΙΟ 2: Ψευδής Σταθερότητα
        if tension < 0.25:
            if abs(current_A) > 0.75 or abs(current_anti_A) > 0.75:
                return 7, stage_info[7]

        # ΚΡΙΤΗΡΙΟ 3: Μόνιμη Διαλεκτική
        if len(self.history_stages) > 20:
            recent_stages = self.history_stages[-20:]
            stage_variability = np.std(recent_stages)
            if stage_variability > 1.8 and np.mean(recent_stages) > 3:
                return 8, stage_info[8]

        # ΚΡΙΤΗΡΙΟ 4: Κανονική ταξινόμηση βάσει έντασης
        if tension < 0.15:
            return 0, stage_info[0]
        elif tension < 0.30:
            return 1, stage_info[1]
        elif tension < 0.45:
            return 2, stage_info[2]
        elif tension < 0.60:
            return 3, stage_info[3]
        elif tension < self.aufhebung_threshold:
            return 4, stage_info[4]
        else:
            return 5, stage_info[5]

    def simulate_step(self, external_A_input):
        """Εκτέλεση ενός βήματος προσομοίωσης"""
        # Ενημέρωση κατάστασης Α
        self.A = np.clip(external_A_input, -1.5, 1.5)

        # 1. Διαλεκτική άρνηση
        current_anti_A = self._dialectical_negation(self.A)

        # 2. Διαλεκτική ένταση
        current_tension = self._calculate_tension(self.A, current_anti_A)

        # 3. Δείκτης XEPTQLRI
        current_XEPTQLRI = self._calculate_XEPTQLRI(current_tension, self.A, current_anti_A)

        # 4. Ταξινόμηση σε στάδιο
        stage_idx, (stage_name, stage_color, stage_icon) = self._classify_stage(
            current_tension, self.A, current_anti_A
        )

        # 5. Καταγραφή
        self.history_A.append(self.A)
        self.history_anti_A.append(current_anti_A)
        self.history_tension.append(current_tension)
        self.history_XEPTQLRI.append(current_XEPTQLRI)
        self.history_stages.append(stage_idx)
        self.history_stage_names.append(stage_name)

        # 6. Ανίχνευση γεγονότων
        if current_XEPTQLRI > 0.8:
            self.risk_events.append({
                'step': len(self.history_A) - 1,
                'XEPTQLRI': current_XEPTQLRI,
                'stage': stage_name,
                'A': self.A,
                'anti_A': current_anti_A,
                'tension': current_tension,
                'icon': '🔴'
            })

        if stage_idx == 6:  # Παράδοξο
            self.paradox_events.append({
                'step': len(self.history_A) - 1,
                'type': 'PARADOXICAL_TRANSCENDENCE',
                'A': self.A,
                'anti_A': current_anti_A,
                'tension': current_tension,
                'icon': '⟡'
            })

        return {
            'A': self.A,
            'anti_A': current_anti_A,
            'tension': current_tension,
            'XEPTQLRI': current_XEPTQLRI,
            'stage': stage_name,
            'stage_idx': stage_idx,
            'stage_color': stage_color,
            'stage_icon': stage_icon
        }

    def get_detailed_report(self):
        """Λεπτομερής αναλυτική έκθεση"""
        if not self.history_XEPTQLRI:
            return {"error": "Δεν υπάρχουν δεδομένα προσομοίωσης"}

        # Στατιστικές
        n_steps = len(self.history_A)
        mean_A = np.mean(self.history_A)
        mean_anti_A = np.mean(self.history_anti_A)
        mean_tension = np.mean(self.history_tension)
        mean_XEPTQLRI = np.mean(self.history_XEPTQLRI)
        max_XEPTQLRI = np.max(self.history_XEPTQLRI)

        # Χρόνος σε διαφορετικές καταστάσεις
        paradox_time = np.mean([1 if s == 6 else 0 for s in self.history_stages]) * 100
        false_stab_time = np.mean([1 if s == 7 else 0 for s in self.history_stages]) * 100
        critical_time = np.mean([1 if s in [5, 6, 7] else 0 for s in self.history_stages]) * 100

        # Συχνότητα σταδίων
        stage_counts = {}
        for idx, (name, color, icon) in self.stages.items():
            count = sum([1 for s in self.history_stages if s == idx])
            stage_counts[name] = count

        # Αξιολόγηση συνολικής κατάστασης
        if paradox_time > 40:
            status = "🔴 ΚΡΙΣΙΜΗ: Υπερβολική Παραδοξότητα"
            risk_level = "ΥΨΗΛΟΣ"
        elif false_stab_time > 50:
            status = "🟠 ΕΠΙΚΙΝΔΥΝΗ: Διερευνητική Ψευδής Σταθερότητα"
            risk_level = "ΜΕΣΟΣ-ΥΨΗΛΟΣ"
        elif max_XEPTQLRI > 2.0:
            status = "🟡 ΠΡΟΣΟΧΗ: Ενδείξεις Ακραίου Κινδύνου"
            risk_level = "ΜΕΣΟΣ"
        elif mean_XEPTQLRI < 0.4:
            status = "🟢 ΣΤΑΘΕΡΗ: Υγιής Διαλεκτική Δυναμική"
            risk_level = "ΧΑΜΗΛΟΣ"
        else:
            status = "🔵 ΔΥΝΑΜΙΚΗ: Ενεργή Διαλεκτική Εξέλιξη"
            risk_level = "ΜΕΣΟΣ"

        report = {
            'system_name': self.system_name,
            'total_steps': n_steps,
            'system_status': status,
            'risk_level': risk_level,
            'final_stage': self.history_stage_names[-1],
            'final_stage_icon': self.stages[self.history_stages[-1]][2],

            'statistics': {
                'mean_A': float(mean_A),
                'mean_anti_A': float(mean_anti_A),
                'mean_tension': float(mean_tension),
                'mean_XEPTQLRI': float(mean_XEPTQLRI),
                'max_XEPTQLRI': float(max_XEPTQLRI),
                'paradox_percentage': float(paradox_time),
                'false_stability_percentage': float(false_stab_time),
                'critical_states_percentage': float(critical_time)
            },

            'events': {
                'risk_events_count': len(self.risk_events),
                'paradox_events_count': len(self.paradox_events),
                'high_risk_events': len([e for e in self.risk_events if e['XEPTQLRI'] > 1.5])
            },

            'stage_distribution': stage_counts,

            'recommendations': self._generate_recommendations(
                paradox_time, false_stab_time, max_XEPTQLRI, mean_XEPTQLRI
            )
        }

        return report

    def _generate_recommendations(self, paradox_time, false_stab_time, max_XEPTQLRI, mean_XEPTQLRI):
        """Δημιουργία συμβουλών βάσει των αποτελεσμάτων"""
        recommendations = []

        if paradox_time > 30:
            recommendations.append("🎭 ΑΥΞΗΜΕΝΗ ΠΑΡΑΔΟΞΟΤΗΤΑ (>30%): Το σύστημα τείνει προς ταυτόχρονες ακραίες καταστάσεις. Εξετάστε διαφορετική αρχιτεκτονική ή δεδομένα εισόδου.")

        if false_stab_time > 40:
            recommendations.append("⚖️ ΨΕΥΔΗΣ ΣΤΑΘΕΡΟΤΗΤΑ (>40%): Η 'σταθερότητα' κρύβει αντιφάσεις. Προσθέστε stochastic components για να 'σπάσετε' την ψευδή ισορροπία.")

        if max_XEPTQLRI > 2.0:
            recommendations.append("⚠️ ΕΞΑΙΡΕΤΙΚΟΣ ΚΙΝΔΥΝΟΣ (XEPTQLRI>2.0): Κοντινό ποιοτικό άλμα. Παρακολουθήστε στενά και ετοιμαστείτε για αλλαγή παραμέτρων.")

        if mean_XEPTQLRI < 0.3 and paradox_time < 10:
            recommendations.append("✅ ΒΕΛΤΙΣΤΗ ΕΠΙΔΟΣΗ: Το σύστημα λειτουργεί σε υγιή διαλεκτική ισορροπία. Συνεχίστε την τρέχουσα προσέγγιση.")

        if len(recommendations) == 0:
            recommendations.append("📊 ΦΥΣΙΟΛΟΓΙΚΗ ΣΥΜΠΕΡΙΦΟΡΑ: Το σύστημα εξελίσσεται φυσιολογικά. Παρακολουθήστε περιοδικά για τυχόν αλλαγές.")

        return recommendations

    def create_interactive_dashboard(self):
        """Δημιουργία διαδραστικού πίνακα ελέγχου"""
        if len(self.history_A) < 20:
            print("⚠️ Χρειάζονται τουλάχιστον 20 βήματα για οπτικοποίηση")
            return None

        fig = plt.figure(figsize=(20, 15))

        # 1. ΚΥΡΙΟ ΓΡΑΦΗΜΑ: A vs ¬A με χρώματα σταδίων
        ax1 = plt.subplot(3, 3, (1, 2))

        # Χρώματα βάσει σταδίου
        colors = [self.stages[s][1] for s in self.history_stages]

        scatter1 = ax1.scatter(range(len(self.history_A)), self.history_A,
                              c=colors, s=40, alpha=0.7, label='A', edgecolors='black', linewidth=0.5)
        scatter2 = ax1.scatter(range(len(self.history_anti_A)), self.history_anti_A,
                              c=colors, s=40, alpha=0.5, marker='s', label='¬A', edgecolors='black', linewidth=0.5)

        # Προσθήκη γραμμών για όρια
        ax1.axhline(y=0.8, color='orange', linestyle='--', alpha=0.6, linewidth=1.5, label='Όριο Ακραίας Τιμής')
        ax1.axhline(y=-0.8, color='orange', linestyle='--', alpha=0.6, linewidth=1.5)
        ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=0.5)

        ax1.set_xlabel('Βήμα Προσομοίωσης', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Τιμή Κατάστασης', fontsize=11, fontweight='bold')
        ax1.set_title('Εξέλιξη Καταστάσεων: A vs ¬A με Χρωματικό Κώδικα Σταδίου',
                     fontsize=13, fontweight='bold', pad=15)
        ax1.legend(loc='upper right', fontsize=9)
        ax1.grid(True, alpha=0.2, linestyle='--')

        # 2. ΧΑΡΤΗΣ ΘΕΡΜΟΤΗΤΑΣ: XEPTQLRI
        ax2 = plt.subplot(3, 3, 3)

        # Δημιουργία χάρτη θερμότητας 2D
        heatmap_data = np.zeros((len(self.history_A), 2))
        heatmap_data[:, 0] = self.history_A
        heatmap_data[:, 1] = self.history_anti_A

        im = ax2.imshow(heatmap_data.T, aspect='auto', cmap='RdYlBu_r',
                       extent=[0, len(self.history_A), -1.5, 1.5])

        ax2.set_xlabel('Βήμα Προσομοίωσης', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Τιμή Κατάστασης', fontsize=11, fontweight='bold')
        ax2.set_title('Χάρτης Θερμότητας: A (πάνω) vs ¬A (κάτω)',
                     fontsize=13, fontweight='bold', pad=15)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)
        plt.colorbar(im, ax=ax2, label='Τιμή (από -1.5 έως 1.5)')

        # 3. ΔΕΙΚΤΗΣ XEPTQLRI ΚΑΙ ΕΝΤΑΣΗ
        ax3 = plt.subplot(3, 3, 4)

        ax3.fill_between(range(len(self.history_tension)), 0, self.history_tension,
                        alpha=0.4, color='green', label='Διαλεκτική Ένταση')
        ax3.plot(self.history_tension, 'g-', linewidth=2, alpha=0.8)

        ax3b = ax3.twinx()
        ax3b.plot(self.history_XEPTQLRI, 'purple', linewidth=2.5, alpha=0.9, label='XEPTQLRI')
        ax3b.fill_between(range(len(self.history_XEPTQLRI)), 0, self.history_XEPTQLRI,
                         alpha=0.2, color='purple')

        # Όρια κινδύνου
        ax3b.axhline(y=0.7, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Προειδοποίηση (0.7)')
        ax3b.axhline(y=1.0, color='red', linestyle='-', linewidth=2, alpha=0.7, label='Κίνδυνος (1.0)')
        ax3b.axhline(y=2.0, color='darkred', linestyle=':', linewidth=2, alpha=0.7, label='Εξαιρετικός (2.0)')

        ax3.set_xlabel('Βήμα Προσομοίωσης', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Διαλεκτική Ένταση', fontsize=11, fontweight='bold', color='green')
        ax3b.set_ylabel('XEPTQLRI', fontsize=11, fontweight='bold', color='purple')
        ax3.set_title('Δείκτης Κινδύνου και Ένταση', fontsize=13, fontweight='bold', pad=15)

        # Συνδυασμός legends
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3b.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

        ax3.grid(True, alpha=0.2, linestyle='--')

        # 4. ΚΑΤΑΝΟΜΗ ΣΤΑΔΙΩΝ (PIE CHART)
        ax4 = plt.subplot(3, 3, 5)

        stage_counts = {}
        for idx, (name, color, icon) in self.stages.items():
            count = sum([1 for s in self.history_stages if s == idx])
            if count > 0:
                stage_counts[name] = count

        if stage_counts:
            labels = [f"{icon} {name.split(':')[1].strip()}"
                     for name in stage_counts.keys()
                     for idx, (s_name, s_color, s_icon) in self.stages.items()
                     if s_name == name]
            sizes = list(stage_counts.values())
            colors_pie = [self.stages[idx][1] for name in stage_counts.keys()
                         for idx, (s_name, _, _) in self.stages.items()
                         if s_name == name]

            wedges, texts, autotexts = ax4.pie(sizes, labels=labels, colors=colors_pie,
                                              autopct='%1.1f%%', startangle=90,
                                              textprops={'fontsize': 9})

            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            ax4.set_title('Κατανομή Διαλεκτικών Σταδίων', fontsize=13, fontweight='bold', pad=15)
        else:
            ax4.text(0.5, 0.5, 'Δεν υπάρχουν δεδομένα\nσταδίων',
                    ha='center', va='center', fontsize=12, transform=ax4.transAxes)
            ax4.set_title('Κατανομή Σταδίων', fontsize=13, fontweight='bold', pad=15)

        # 5. ΦΑΣΜΑ Α vs ¬A (SCATTER 2D)
        ax5 = plt.subplot(3, 3, 6)

        scatter = ax5.scatter(self.history_A, self.history_anti_A,
                             c=self.history_XEPTQLRI, cmap='RdYlBu_r',
                             s=50, alpha=0.7, edgecolors='black', linewidth=0.5)

        # Ζώνες παραδόξου
        from matplotlib.patches import Rectangle
        ax5.add_patch(Rectangle((0.8, 0.8), 0.7, 0.7, alpha=0.15, color='red',
                               label='Ζώνη Παραδόξου I'))
        ax5.add_patch(Rectangle((-1.5, -1.5), 0.7, 0.7, alpha=0.15, color='red',
                               label='Ζώνη Παραδόξου II'))

        ax5.set_xlabel('Τιμή A', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Τιμή ¬A', fontsize=11, fontweight='bold')
        ax5.set_title('Φάσμα Καταστάσεων με XEPTQLRI', fontsize=13, fontweight='bold', pad=15)
        ax5.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax5.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        ax5.set_xlim(-1.5, 1.5)
        ax5.set_ylim(-1.5, 1.5)
        ax5.grid(True, alpha=0.2, linestyle='--')
        plt.colorbar(scatter, ax=ax5, label='XEPTQLRI')

        # 6. ΙΣΤΟΡΙΚΗ ΕΞΕΛΙΞΗ ΣΤΑΔΙΩΝ
        ax6 = plt.subplot(3, 3, (7, 8))

        # Χάρτης θερμότητας σταδίων
        stage_matrix = np.array(self.history_stages).reshape(1, -1)
        im_stage = ax6.imshow(stage_matrix, aspect='auto', cmap='tab10',
                             extent=[0, len(self.history_stages), 0, 1])

        ax6.set_xlabel('Βήμα Προσομοίωσης', fontsize=11, fontweight='bold')
        ax6.set_yticks([0.5])
        ax6.set_yticklabels(['Στάδιο'], fontsize=11, fontweight='bold')
        ax6.set_title('Ιστορική Εξέλιξη Σταδίων', fontsize=13, fontweight='bold', pad=15)

        # Προσθήκη κάθετης γραμμής για τρέχον βήμα
        current_step = len(self.history_stages) - 1
        ax6.axvline(x=current_step, color='white', linestyle='--', linewidth=2, alpha=0.8)

        # Προσθήκη legend για τα στάδια
        from matplotlib.patches import Patch
        legend_elements = []
        for idx in sorted(set(self.history_stages)):
            name, color, icon = self.stages[idx]
            legend_elements.append(Patch(facecolor=color, edgecolor='black',
                                        label=f"{icon} {name.split(':')[0]}"))

        ax6.legend(handles=legend_elements, loc='upper right', fontsize=8, ncol=2)

        # 7. ΑΝΑΛΥΤΙΚΗ ΕΚΘΕΣΗ (TEXT)
        ax7 = plt.subplot(3, 3, 9)
        ax7.axis('off')

        report = self.get_detailed_report()

        if 'error' not in report:
            stats = report['statistics']
            events = report['events']

            text_content = (
                f"📊 ΑΝΑΛΥΤΙΚΗ ΕΚΘΕΣΗ\n"
                f"{'='*30}\n"
                f"Σύστημα: {report['system_name']}\n"
                f"Βήματα: {report['total_steps']}\n"
                f"Τελικό Στάδιο: {report['final_stage_icon']} {report['final_stage']}\n"
                f"Κατάσταση: {report['system_status']}\n"
                f"Επίπεδο Κινδύνου: {report['risk_level']}\n\n"

                f"📈 ΣΤΑΤΙΣΤΙΚΑ:\n"
                f"• Μέσος XEPTQLRI: {stats['mean_XEPTQLRI']:.3f}\n"
                f"• Μέγιστος XEPTQLRI: {stats['max_XEPTQLRI']:.3f}\n"
                f"• Παραδοξότητα: {stats['paradox_percentage']:.1f}%\n"
                f"• Ψευδής Σταθερότητα: {stats['false_stability_percentage']:.1f}%\n"
                f"• Κρίσιμες Καταστάσεις: {stats['critical_states_percentage']:.1f}%\n\n"

                f"⚠️  ΓΕΓΟΝΟΤΑ:\n"
                f"• Γεγονότα Κινδύνου: {events['risk_events_count']}\n"
                f"• Γεγονότα Παραδόξου: {events['paradox_events_count']}\n"
                f"• Υψηλού Κινδύνου: {events['high_risk_events']}\n"
            )

            ax7.text(0.05, 0.95, text_content, transform=ax7.transAxes,
                    fontsize=9, family='monospace', verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='#f8f9fa', alpha=0.9,
                            edgecolor='#dee2e6', linewidth=2))

            # Προσθήκη συμβουλών
            if report['recommendations']:
                rec_text = "\n💡 ΣΥΜΒΟΥΛΕΣ:\n"
                for i, rec in enumerate(report['recommendations'], 1):
                    rec_text += f"{i}. {rec}\n"

                ax7.text(0.05, 0.05, rec_text, transform=ax7.transAxes,
                        fontsize=8, family='sans-serif', verticalalignment='bottom',
                        bbox=dict(boxstyle='round', facecolor='#fff3cd', alpha=0.8,
                                edgecolor='#ffeaa7', linewidth=1.5))

        plt.suptitle(f'ΔΙΑΔΡΑΣΤΙΚΟΣ ΠΙΝΑΚΑΣ ΕΛΕΓΧΟΥ: {self.system_name}\n',
                    fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        return fig

print("✅ Πυρήνας Συστήματος Ξενόπουλου ολοκληρώθηκε!")

# ============================================
# ΒΕΛΤΙΩΜΕΝΟ LSTM ΜΟΝΤΕΛΟ
# ============================================

def generate_quantum_data(num_samples, timesteps=20, noise_level=0.5, seed=None):
    """Βελτιωμένη δημιουργία δεδομένων με έλεγχο θορύβου"""
    if seed is not None:
        np.random.seed(seed)

    # Καθαρές καταστάσεις με πιο ρεαλιστική δομή
    phase = np.random.uniform(0, 2*np.pi, (num_samples, 1, 1))
    amplitude = np.random.uniform(0.5, 1.5, (num_samples, timesteps, 3))

    clean_real = amplitude * np.cos(np.linspace(0, 4*np.pi, timesteps).reshape(1, -1, 1) + phase)
    clean_imag = amplitude * np.sin(np.linspace(0, 4*np.pi, timesteps).reshape(1, -1, 1) + phase)

    clean_states = clean_real + 1j * clean_imag
    clean_states = clean_states / (np.linalg.norm(clean_states, axis=-1, keepdims=True) + 1e-8)

    # Προσθετικός και πολλαπλασιαστικός θόρυβος
    additive_noise = noise_level * np.random.randn(*clean_states.shape)
    multiplicative_noise = 1 + (noise_level * 0.3) * np.random.randn(*clean_states.shape)

    noisy_states = clean_states * multiplicative_noise + additive_noise

    # Κανονικοποίηση
    noisy_states = noisy_states / (np.linalg.norm(noisy_states, axis=-1, keepdims=True) + 1e-8)

    # Μετατροπή σε πραγματικές/φανταστικές συνιστώσες
    noisy_states = np.float32(np.concatenate([noisy_states.real, noisy_states.imag], axis=-1))
    clean_states = np.float32(np.concatenate([clean_states.real, clean_states.imag], axis=-1))

    return noisy_states, clean_states

def build_advanced_lstm_model(timesteps=20, input_dim=6, lstm_units=[128, 64], dropout_rate=0.3):
    """Βελτιωμένο LSTM μοντέλο με παραμετροποίηση"""
    input_layer = Input(shape=(timesteps, input_dim))

    # Προ-επεξεργασία με καλύτερη κλιμάκωση
    x = Rescaling(1./np.sqrt(input_dim))(input_layer)

    # Δυναμική αρχιτεκτονική
    for i, units in enumerate(lstm_units):
        return_sequences = (i < len(lstm_units) - 1)
        x = LSTM(units, return_sequences=return_sequences,
                activation='tanh', recurrent_activation='sigmoid',
                kernel_initializer='glorot_uniform')(x)

        if i < len(lstm_units) - 1:  # Dropout μόνο σε ενδιάμεσα στρώματα
            x = Dropout(dropout_rate)(x)

    # Επανάληψη για sequence output
    if not lstm_units[-1] == timesteps:
        x = tf.keras.layers.RepeatVector(timesteps)(x)
        x = LSTM(32, return_sequences=True)(x)

    # Βελτιωμένο output layer
    x = Dense(64, activation='relu')(x)
    x = Dropout(dropout_rate * 0.5)(x)
    x = Dense(32, activation='relu')(x)
    output = Dense(input_dim, activation='linear')(x)

    model = Model(inputs=input_layer, outputs=output)
    return model

print("✅ LSTM μοντέλο ορίστηκε!")

# ============================================
# ΔΙΑΔΡΑΣΤΙΚΟ ΠΑΡΑΘΥΡΟ ΕΛΕΓΧΟΥ
# ============================================

class InteractiveXenopoulosAnalyzer:
    """Πλήρως διαδραστική ανάλυση LSTM με Ξενόπουλο"""

    def __init__(self):
        self.timesteps = 20
        self.input_dim = 6
        self.model = None
        self.xenopoulos_systems = []
        self.analysis_results = {}
        self.setup_widgets()

    def setup_widgets(self):
        """Δημιουργία διαδραστικών widgets"""
        print("🛠️  Δημιουργία διαδραστικού πίνακα ελέγχου...")

        # WIDGETS ΠΑΡΑΜΕΤΡΩΝ
        self.num_samples_slider = widgets.IntSlider(
            value=2000, min=500, max=10000, step=500,
            description='Δείγματα:', style={'description_width': 'initial'}
        )

        self.noise_level_slider = widgets.FloatSlider(
            value=0.3, min=0.1, max=1.0, step=0.1,
            description='Θόρυβος:', style={'description_width': 'initial'}
        )

        self.epochs_slider = widgets.IntSlider(
            value=30, min=10, max=100, step=5,
            description='Epochs:', style={'description_width': 'initial'}
        )

        self.lstm_units_dropdown = widgets.Dropdown(
            options=['[64, 32]', '[128, 64]', '[256, 128, 64]', '[512, 256, 128]'],
            value='[128, 64]',
            description='LSTM Units:', style={'description_width': 'initial'}
        )

        self.dropout_slider = widgets.FloatSlider(
            value=0.3, min=0.1, max=0.7, step=0.05,
            description='Dropout:', style={'description_width': 'initial'}
        )

        self.xen_steps_slider = widgets.IntSlider(
            value=100, min=50, max=500, step=50,
            description='Βήματα Ξενόπουλου:', style={'description_width': 'initial'}
        )

        # ΚΟΥΜΠΙΑ ΕΛΕΓΧΟΥ
        self.train_button = widgets.Button(
            description='🚀 Εκπαίδευση & Ανάλυση',
            button_style='success',
            tooltip='Εκτέλεση πλήρους ανάλυσης',
            layout=widgets.Layout(width='300px', height='40px')
        )

        self.visualize_button = widgets.Button(
            description='📊 Οπτικοποίηση Αποτελεσμάτων',
            button_style='info',
            tooltip='Εμφάνιση γραφημάτων',
            disabled=True,
            layout=widgets.Layout(width='300px', height='40px')
        )

        self.export_button = widgets.Button(
            description='💾 Εξαγωγή Αναφοράς',
            button_style='warning',
            tooltip='Εξαγωγή δεδομένων',
            disabled=True,
            layout=widgets.Layout(width='300px', height='40px')
        )

        # OUTPUT AREA
        self.output_area = widgets.Output(layout={'border': '1px solid #ccc', 'padding': '10px'})

        # ΣΥΝΔΕΣΗ ΚΟΥΜΠΙΩΝ
        self.train_button.on_click(self.run_full_analysis)
        self.visualize_button.on_click(self.visualize_results)
        self.export_button.on_click(self.export_report)

        # ΟΡΓΑΝΩΣΗ ΠΛΑΙΣΙΟΥ
        params_box = widgets.VBox([
            widgets.HTML("<h3>📋 Παράμετροι Μοντέλου</h3>"),
            self.num_samples_slider,
            self.noise_level_slider,
            self.epochs_slider,
            self.lstm_units_dropdown,
            self.dropout_slider,
            self.xen_steps_slider,
            widgets.HTML("<br>")
        ], layout=widgets.Layout(width='50%'))

        control_box = widgets.VBox([
            widgets.HTML("<h3>🎮 Έλεγχος</h3>"),
            self.train_button,
            widgets.HTML("<br>"),
            self.visualize_button,
            widgets.HTML("<br>"),
            self.export_button
        ], layout=widgets.Layout(width='30%'))

        main_box = widgets.HBox([params_box, control_box])

        display(widgets.VBox([
            widgets.HTML("<h1 style='color: #2c3e50;'>🔬 Διαλεκτική Ανάλυση LSTM με Σύστημα Ξενόπουλου</h1>"),
            widgets.HTML("<p style='font-size: 14px;'>Πλήρως διαδραστική ανάλυση LSTM denoising μοντέλου με το Γενετικο-Ιστορικό Σύστημα Λογικής Ξενόπουλου</p>"),
            main_box,
            self.output_area
        ]))

        print("✅ Διαδραστικός πίνακας ελέγχου έτοιμος!")

    def run_full_analysis(self, b):
        """Εκτέλεση πλήρους ανάλυσης"""
        with self.output_area:
            clear_output()
            print("="*70)
            print("🚀 ΕΝΑΡΞΗ ΠΛΗΡΟΥΣ ΑΝΑΛΥΣΗΣ")
            print("="*70)

            # 1. ΔΗΜΙΟΥΡΓΙΑ ΔΕΔΟΜΕΝΩΝ
            print("\n📁 ΒΗΜΑ 1: Δημιουργία δεδομένων...")
            X, y = generate_quantum_data(
                self.num_samples_slider.value,
                self.timesteps,
                self.noise_level_slider.value,
                seed=42
            )

            # Split
            split = int(0.8 * len(X))
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            print(f"   • Training samples: {len(X_train)}")
            print(f"   • Test samples: {len(X_test)}")
            print(f"   • Shape: {X_train.shape}")

            # 2. ΚΑΤΑΣΚΕΥΗ ΜΟΝΤΕΛΟΥ
            print("\n🏗️  ΒΗΜΑ 2: Κατασκευή LSTM μοντέλου...")
            lstm_units = eval(self.lstm_units_dropdown.value)

            self.model = build_advanced_lstm_model(
                timesteps=self.timesteps,
                input_dim=self.input_dim,
                lstm_units=lstm_units,
                dropout_rate=self.dropout_slider.value
            )

            self.model.compile(
                optimizer=Adam(learning_rate=0.001, clipnorm=1.0),
                loss='mse',
                metrics=['mae', 'mse']
            )

            self.model.summary(print_fn=lambda x: print(f"   {x}"))

            # 3. ΕΚΠΑΙΔΕΥΣΗ
            print("\n📚 ΒΗΜΑ 3: Εκπαίδευση μοντέλου...")
            history = self.model.fit(
                X_train, y_train,
                epochs=self.epochs_slider.value,
                batch_size=64,
                validation_split=0.2,
                callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
                verbose=1
            )

            # 4. ΑΞΙΟΛΟΓΗΣΗ
            print("\n📊 ΒΗΜΑ 4: Αξιολόγηση απόδοσης...")
            test_results = self.model.evaluate(X_test, y_test, verbose=0)
            test_mae = test_results[1]
            test_mse = test_results[2]

            # Baseline
            baseline_mae = np.mean(np.abs(X_test - y_test))
            improvement = baseline_mae - test_mae
            improvement_pct = (improvement / baseline_mae) * 100

            print(f"   • Test MAE: {test_mae:.4f}")
            print(f"   • Test MSE: {test_mse:.4f}")
            print(f"   • Baseline MAE: {baseline_mae:.4f}")
            print(f"   • Βελτίωση: {improvement:.4f} ({improvement_pct:.1f}%)")

            # 5. ΔΙΑΛΕΚΤΙΚΗ ΑΝΑΛΥΣΗ ΜΕ ΞΕΝΟΠΟΥΛΟ
            print("\n🔮 ΒΗΜΑ 5: Διαλεκτική ανάλυση με Ξενόπουλο...")

            # Πρόβλεψη
            predictions = self.model.predict(X_test, verbose=0)

            # Υπολογισμός MAE ανά timestep
            mae_per_sample_timestep = np.abs(predictions - y_test)
            mae_per_timestep = np.mean(mae_per_sample_timestep, axis=(0, 2))

            # Αρχικοποίηση συστημάτων Ξενόπουλου
            self.xenopoulos_systems = []
            for step in range(self.timesteps):
                # Μετατροπή MAE σε κατάσταση Α (0=τέλειο, 1=χειρότερο)
                A_value = np.clip(1.0 - (mae_per_timestep[step] * 8), -1.0, 1.0)

                system = XenopoulosSystem(
                    initial_state_A=A_value,
                    historical_horizon=self.xen_steps_slider.value,
                    aufhebung_threshold=0.8,
                    system_name=f"LSTM_Step_{step}_MAE{mae_per_timestep[step]:.3f}"
                )

                # Προσομοίωση
                for i in range(self.xen_steps_slider.value):
                    # Προσθήκη τυχαιότητας που εξαρτάται από το MAE
                    noise_level = 0.05 + mae_per_timestep[step] * 0.1
                    A_with_noise = A_value + np.random.normal(0, noise_level)
                    system.simulate_step(A_with_noise)

                self.xenopoulos_systems.append(system)

            # 6. ΣΥΓΚΕΝΤΡΩΤΙΚΗ ΑΝΑΛΥΣΗ
            print("\n📋 ΒΗΜΑ 6: Συγκεντρωτική ανάλυση αποτελεσμάτων...")

            all_reports = []
            high_risk_steps = []
            paradox_steps = []

            for step, system in enumerate(self.xenopoulos_systems):
                report = system.get_detailed_report()
                all_reports.append(report)

                if report['statistics']['max_XEPTQLRI'] > 1.0:
                    high_risk_steps.append((step, report['statistics']['max_XEPTQLRI']))

                if report['statistics']['paradox_percentage'] > 20.0:
                    paradox_steps.append((step, report['statistics']['paradox_percentage']))

            # Υπολογισμός μέσων όρων
            mean_XEPTQLRI = np.mean([r['statistics']['mean_XEPTQLRI'] for r in all_reports])
            mean_paradox = np.mean([r['statistics']['paradox_percentage'] for r in all_reports])
            mean_false_stab = np.mean([r['statistics']['false_stability_percentage'] for r in all_reports])

            # Αποθήκευση αποτελεσμάτων
            self.analysis_results = {
                'test_mae': test_mae,
                'test_mse': test_mse,
                'baseline_mae': baseline_mae,
                'improvement': improvement,
                'improvement_pct': improvement_pct,
                'mae_per_timestep': mae_per_timestep,
                'all_reports': all_reports,
                'high_risk_steps': high_risk_steps,
                'paradox_steps': paradox_steps,
                'mean_XEPTQLRI': mean_XEPTQLRI,
                'mean_paradox': mean_paradox,
                'mean_false_stab': mean_false_stab,
                'model_history': history.history,
                'predictions': predictions,
                'X_test': X_test,
                'y_test': y_test
            }

            # 7. ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
            print("\n" + "="*70)
            print("📈 ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΛΥΣΗΣ")
            print("="*70)

            print(f"\n📊 ΣΤΑΤΙΣΤΙΚΑ ΜΟΝΤΕΛΟΥ:")
            print(f"   • Test MAE: {test_mae:.4f}")
            print(f"   • Βελτίωση vs Baseline: {improvement_pct:.1f}%")

            print(f"\n⚠️  ΑΝΙΧΝΕΥΣΗ ΚΙΝΔΥΝΟΥ ΞΕΝΟΠΟΥΛΟΥ:")
            print(f"   • Μέσος XEPTQLRI: {mean_XEPTQLRI:.3f}")
            print(f"   • Μέση Παραδοξότητα: {mean_paradox:.1f}%")
            print(f"   • Μέση Ψευδής Σταθ.: {mean_false_stab:.1f}%")
            print(f"   • Βήματα με κίνδυνο: {len(high_risk_steps)}/{self.timesteps}")
            print(f"   • Βήματα με παράδοξο: {len(paradox_steps)}/{self.timesteps}")

            if high_risk_steps:
                print(f"\n🔴 ΒΗΜΑΤΑ ΥΨΗΛΟΥ ΚΙΝΔΥΝΟΥ (XEPTQLRI > 1.0):")
                for step, risk in sorted(high_risk_steps, key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   • Βήμα {step}: XEPTQLRI = {risk:.2f}, MAE = {mae_per_timestep[step]:.4f}")

            if paradox_steps:
                print(f"\n⟡ ΒΗΜΑΤΑ ΥΨΗΛΗΣ ΠΑΡΑΔΟΞΟΤΗΤΑΣ (>20%):")
                for step, paradox in sorted(paradox_steps, key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   • Βήμα {step}: Παραδοξότητα = {paradox:.1f}%, MAE = {mae_per_timestep[step]:.4f}")

            # Αξιολόγηση συνολικής κατάστασης
            print(f"\n📌 ΣΥΝΟΛΙΚΗ ΔΙΑΓΝΩΣΗ:")
            if mean_paradox > 35:
                print(f"   🔴 ΚΡΙΣΙΜΗ: Το μοντέλο λειτουργεί σε παθολογική παραδοξότητα")
                print(f"   💡 ΠΡΟΤΑΣΗ: Επανασχεδίαση αρχιτεκτονικής ή training data")
            elif len(high_risk_steps) > self.timesteps / 2:
                print(f"   🟠 ΕΠΙΚΙΝΔΥΝΗ: Πολλαπλά σημεία κινδύνου ποιοτικής αλλαγής")
                print(f"   💡 ΠΡΟΤΑΣΗ: Προσθήκη regularization και επανεκπαίδευση")
            elif mean_false_stab > 40:
                print(f"   🟡 ΠΡΟΣΟΧΗ: Υψηλή πιθανότητα ψευδούς σταθερότητας")
                print(f"   💡 ΠΡΟΤΑΣΗ: Προσθήκη noise και data augmentation")
            else:
                print(f"   🟢 ΚΑΛΗ: Υγιής διαλεκτική συμπεριφορά")
                print(f"   💡 ΠΡΟΤΑΣΗ: Συνεχίστε την τρέχουσα προσέγγιση")

            # Ενεργοποίηση κουμπιών
            self.visualize_button.disabled = False
            self.export_button.disabled = False

            print(f"\n✅ Η ανάλυση ολοκληρώθηκε επιτυχώς!")
            print(f"   Κάντε κλικ στο 'Οπτικοποίηση Αποτελεσμάτων' για τα γραφήματα.")

    def visualize_results(self, b):
        """Οπτικοποίηση όλων των αποτελεσμάτων"""
        with self.output_area:
            clear_output()
            print("🎨 ΔΗΜΙΟΥΡΓΙΑ ΟΠΤΙΚΟΠΟΙΗΣΕΩΝ...")

            if not self.analysis_results:
                print("⚠️  Δεν υπάρχουν αποτελέσματα. Εκτελέστε πρώτα την ανάλυση.")
                return

            # Δημιουργία πολλαπλών figures
            self.create_summary_figure()
            self.create_detailed_figures()

            print("\n✅ Όλες οι οπτικοποιήσεις δημιουργήθηκαν!")
            print("   Τα γραφήματα εμφανίζονται παρακάτω.")

    def create_summary_figure(self):
        """Δημιουργία συνοπτικού figure"""
        fig = plt.figure(figsize=(20, 12))

        # 1. MAE ανά timestep με κίνδυνο
        ax1 = plt.subplot(2, 3, 1)
        mae = self.analysis_results['mae_per_timestep']
        timesteps = range(len(mae))

        bars = ax1.bar(timesteps, mae, alpha=0.7, edgecolor='black')

        # Χρώμα βάσει κινδύνου
        for i, (step, value) in enumerate(zip(timesteps, mae)):
            # Έλεγχος αν το βήμα είναι επικίνδυνο
            is_risky = any(step == risky_step for risky_step, _ in self.analysis_results['high_risk_steps'])
            is_paradox = any(step == paradox_step for paradox_step, _ in self.analysis_results['paradox_steps'])

            if is_paradox:
                bars[i].set_color('#8A2BE2')  # Μωβ για παράδοξο
                bars[i].set_hatch('//')
            elif is_risky:
                bars[i].set_color('#DC143C')  # Κόκκινο για κίνδυνο
                bars[i].set_hatch('\\')
            elif value > np.mean(mae) * 1.2:
                bars[i].set_color('#FFA500')  # Πορτοκαλί για υψηλό MAE

        ax1.axhline(y=np.mean(mae), color='blue', linestyle='--',
                   label=f'Μέσος MAE: {np.mean(mae):.4f}')
        ax1.set_xlabel('Χρονικό Βήμα')
        ax1.set_ylabel('MAE')
        ax1.set_title('Απόδοση ανά Βήμα με Ένδειξη Κινδύνου')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # 2. Σύγκριση XEPTQLRI ανά βήμα
        ax2 = plt.subplot(2, 3, 2)
        max_XEPTQLRI = [r['statistics']['max_XEPTQLRI'] for r in self.analysis_results['all_reports']]
        mean_XEPTQLRI = [r['statistics']['mean_XEPTQLRI'] for r in self.analysis_results['all_reports']]

        ax2.plot(timesteps, max_XEPTQLRI, 'r-o', linewidth=2, markersize=6, label='Max XEPTQLRI')
        ax2.plot(timesteps, mean_XEPTQLRI, 'b-s', linewidth=2, markersize=4, alpha=0.7, label='Mean XEPTQLRI')

        ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Κίνδυνος (1.0)')
        ax2.axhline(y=0.7, color='orange', linestyle=':', alpha=0.7, label='Προειδοποίηση (0.7)')

        ax2.set_xlabel('Χρονικό Βήμα')
        ax2.set_ylabel('XEPTQLRI')
        ax2.set_title('Δείκτης Κινδύνου Ξενόπουλου ανά Βήμα')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Παραδοξότητα vs Ψευδής Σταθερότητα
        ax3 = plt.subplot(2, 3, 3)

        paradox = [r['statistics']['paradox_percentage'] for r in self.analysis_results['all_reports']]
        false_stab = [r['statistics']['false_stability_percentage'] for r in self.analysis_results['all_reports']]

        width = 0.35
        x = np.arange(len(paradox))
        ax3.bar(x - width/2, paradox, width, label='Παραδοξότητα %', color='purple', alpha=0.7)
        ax3.bar(x + width/2, false_stab, width, label='Ψευδής Σταθ. %', color='orange', alpha=0.7)

        ax3.axhline(y=20, color='purple', linestyle=':', alpha=0.5, label='Όριο Παραδόξου')
        ax3.axhline(y=30, color='orange', linestyle=':', alpha=0.5, label='Όριο Ψευδούς Σταθ.')

        ax3.set_xlabel('Χρονικό Βήμα')
        ax3.set_ylabel('Ποσοστό (%)')
        ax3.set_title('Παραδοξότητα vs Ψευδής Σταθερότητα')
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3, axis='y')

        # 4. Ιστορικό εκπαίδευσης
        ax4 = plt.subplot(2, 3, 4)

        history = self.analysis_results['model_history']
        epochs = range(1, len(history['loss']) + 1)

        ax4.plot(epochs, history['loss'], 'b-', label='Training Loss', linewidth=2)
        ax4.plot(epochs, history['val_loss'], 'r--', label='Validation Loss', linewidth=2)
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Loss (MSE)')
        ax4.set_title('Ιστορικό Εκπαίδευσης')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # 5. Heatmap των προβλέψεων vs πραγματικών τιμών (πρώτο δείγμα)
        ax5 = plt.subplot(2, 3, 5)

        if 'predictions' in self.analysis_results:
            sample_idx = 0
            predictions_sample = self.analysis_results['predictions'][sample_idx]
            actual_sample = self.analysis_results['y_test'][sample_idx]

            # Διαφορά
            diff = np.abs(predictions_sample - actual_sample)

            im = ax5.imshow(diff.T, aspect='auto', cmap='YlOrRd')
            ax5.set_xlabel('Χρονικό Βήμα')
            ax5.set_ylabel('Διαστάσεις')
            ax5.set_title('Απόλυτη Διαφορά: Πρόβλεψη vs Πραγματικό (πρώτο δείγμα)')
            plt.colorbar(im, ax=ax5, label='Απόλυτη Διαφορά')

        # 6. Συνοπτική εκθεση
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')

        summary_text = (
            f"📋 ΣΥΝΟΠΤΙΚΗ ΑΝΑΛΥΣΗ\n"
            f"{'='*30}\n"
            f"• Δείγματα: {self.num_samples_slider.value}\n"
            f"• Epochs: {self.epochs_slider.value}\n"
            f"• Test MAE: {self.analysis_results['test_mae']:.4f}\n"
            f"• Βελτίωση: {self.analysis_results['improvement_pct']:.1f}%\n\n"

            f"⚠️  ΚΙΝΔΥΝΟΙ ΞΕΝΟΠΟΥΛΟΥ:\n"
            f"• Μέσος XEPTQLRI: {self.analysis_results['mean_XEPTQLRI']:.3f}\n"
            f"• Μέση Παραδοξότητα: {self.analysis_results['mean_paradox']:.1f}%\n"
            f"• Βήματα κινδύνου: {len(self.analysis_results['high_risk_steps'])}\n"
            f"• Βήματα παραδόξου: {len(self.analysis_results['paradox_steps'])}\n"
        )

        ax6.text(0.05, 0.95, summary_text, transform=ax6.transAxes,
                fontsize=10, family='monospace', verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#f8f9fa', alpha=0.9))

        plt.suptitle('ΣΥΝΟΠΤΙΚΗ ΑΝΑΛΥΣΗ LSTM ΜΟΝΤΕΛΟΥ ΜΕ ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ',
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()

    def create_detailed_figures(self):
        """Δημιουργία λεπτομερών figures για κάθε σύστημα Ξενόπουλου"""
        print("\n📊 Δημιουργία λεπτομερών αναφορών ανά βήμα...")

        # Επιλογή μόνο των πιο ενδιαφερόντων βημάτων
        interesting_steps = []

        # Βήματα με υψηλό κίνδυνο
        for step, _ in self.analysis_results['high_risk_steps'][:3]:
            interesting_steps.append(step)

        # Βήματα με παράδοξο
        for step, _ in self.analysis_results['paradox_steps'][:3]:
            if step not in interesting_steps:
                interesting_steps.append(step)

        # Βήματα με υψηλό MAE
        mae = self.analysis_results['mae_per_timestep']
        high_mae_indices = np.argsort(mae)[-3:][::-1]
        for step in high_mae_indices:
            if step not in interesting_steps:
                interesting_steps.append(step)

        # Βήματα με χαμηλό MAE
        low_mae_indices = np.argsort(mae)[:3]
        for step in low_mae_indices:
            if step not in interesting_steps:
                interesting_steps.append(step)

        # Δημιουργία dashboard για κάθε ενδιαφέρον βήμα
        for i, step in enumerate(sorted(set(interesting_steps))[:6]):  # Μέχρι 6 βήματα
            if step < len(self.xenopoulos_systems):
                system = self.xenopoulos_systems[step]
                report = self.analysis_results['all_reports'][step]

                print(f"\n📈 Βήμα {step} (MAE: {mae[step]:.4f}):")
                print(f"   • Στάδιο: {report['final_stage']}")
                print(f"   • Max XEPTQLRI: {report['statistics']['max_XEPTQLRI']:.2f}")
                print(f"   • Παραδοξότητα: {report['statistics']['paradox_percentage']:.1f}%")

                # Δημιουργία dashboard
                fig = system.create_interactive_dashboard()
                if fig:
                    plt.show()

    def export_report(self, b):
        """Εξαγωγή αναφοράς"""
        with self.output_area:
            clear_output()
            print("💾 ΕΞΑΓΩΓΗ ΑΝΑΦΟΡΑΣ...")

            if not self.analysis_results:
                print("⚠️  Δεν υπάρχουν αποτελέσματα για εξαγωγή.")
                return

            # Δημιουργία αναφοράς
            timestamp = np.datetime64('now').astype(str).replace(':', '-')
            filename = f"xenopoulos_lstm_analysis_{timestamp}.txt"

            report_content = self.generate_text_report()

            # Εμφάνιση αναφοράς
            print("\n" + "="*70)
            print("📄 ΑΝΑΛΥΤΙΚΗ ΕΚΘΕΣΗ")
            print("="*70)
            print(report_content)

            # Προσφορά για αποθήκευση
            print(f"\n💾 Η αναφορά μπορεί να αποθηκευτεί ως: {filename}")
            print("   Αντιγράψτε το παραπάνω κείμενο και αποθηκεύστε το σε αρχείο .txt")

            # Επίσης δημιουργούμε ένα συνοπτικό DataFrame
            import pandas as pd

            summary_data = []
            for step, report in enumerate(self.analysis_results['all_reports']):
                stats = report['statistics']
                summary_data.append({
                    'Step': step,
                    'MAE': self.analysis_results['mae_per_timestep'][step],
                    'Mean_XEPTQLRI': stats['mean_XEPTQLRI'],
                    'Max_XEPTQLRI': stats['max_XEPTQLRI'],
                    'Paradox_%': stats['paradox_percentage'],
                    'False_Stability_%': stats['false_stability_percentage'],
                    'Stage': report['final_stage'].split(':')[1].strip()[:20]
                })

            df_summary = pd.DataFrame(summary_data)
            print(f"\n📊 ΣΥΝΟΠΤΙΚΟΣ ΠΙΝΑΚΑΣ (πρώτες 5 γραμμές):")
            print(df_summary.head().to_string())

    def generate_text_report(self):
        """Δημιουργία κειμενικής αναφοράς"""
        report = []

        report.append("="*70)
        report.append("ΔΙΑΛΕΚΤΙΚΗ ΑΝΑΛΥΣΗ LSTM ΜΟΝΤΕΛΟΥ ΜΕ ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ")
        report.append("="*70)
        report.append(f"Ημερομηνία ανάλυσης: {np.datetime64('now')}")
        report.append(f"Παράμετροι μοντέλου: {self.num_samples_slider.value} δείγματα, "
                     f"{self.epochs_slider.value} epochs, θόρυβος {self.noise_level_slider.value}")
        report.append("")

        # Στατιστικά μοντέλου
        report.append("📊 ΣΤΑΤΙΣΤΙΚΑ ΜΟΝΤΕΛΟΥ:")
        report.append(f"  • Test MAE: {self.analysis_results['test_mae']:.4f}")
        report.append(f"  • Test MSE: {self.analysis_results['test_mse']:.4f}")
        report.append(f"  • Baseline MAE: {self.analysis_results['baseline_mae']:.4f}")
        report.append(f"  • Βελτίωση: {self.analysis_results['improvement_pct']:.1f}%")
        report.append("")

        # Στατιστικά Ξενόπουλου
        report.append("⚠️  ΣΤΑΤΙΣΤΙΚΑ ΚΙΝΔΥΝΟΥ ΞΕΝΟΠΟΥΛΟΥ:")
        report.append(f"  • Μέσος XEPTQLRI: {self.analysis_results['mean_XEPTQLRI']:.3f}")
        report.append(f"  • Μέση Παραδοξότητα: {self.analysis_results['mean_paradox']:.1f}%")
        report.append(f"  • Μέση Ψευδής Σταθερότητα: {self.analysis_results['mean_false_stab']:.1f}%")
        report.append(f"  • Βήματα με κίνδυνο (XEPTQLRI > 1.0): {len(self.analysis_results['high_risk_steps'])}")
        report.append(f"  • Βήματα με παράδοξο (>20%): {len(self.analysis_results['paradox_steps'])}")
        report.append("")

        # Πιο επικίνδυνα βήματα
        if self.analysis_results['high_risk_steps']:
            report.append("🔴 ΒΗΜΑΤΑ ΥΨΗΛΟΥ ΚΙΝΔΥΝΟΥ:")
            for step, risk in sorted(self.analysis_results['high_risk_steps'],
                                   key=lambda x: x[1], reverse=True):
                mae = self.analysis_results['mae_per_timestep'][step]
                paradox = self.analysis_results['all_reports'][step]['statistics']['paradox_percentage']
                report.append(f"  • Βήμα {step}: XEPTQLRI={risk:.2f}, MAE={mae:.4f}, "
                            f"Παραδοξότητα={paradox:.1f}%")
            report.append("")

        # Βήματα με παράδοξο
        if self.analysis_results['paradox_steps']:
            report.append("⟡ ΒΗΜΑΤΑ ΜΕ ΥΨΗΛΗ ΠΑΡΑΔΟΞΟΤΗΤΑ:")
            for step, paradox in sorted(self.analysis_results['paradox_steps'],
                                      key=lambda x: x[1], reverse=True):
                mae = self.analysis_results['mae_per_timestep'][step]
                xeptqlri = self.analysis_results['all_reports'][step]['statistics']['max_XEPTQLRI']
                report.append(f"  • Βήμα {step}: Παραδοξότητα={paradox:.1f}%, "
                            f"MAE={mae:.4f}, Max XEPTQLRI={xeptqlri:.2f}")
            report.append("")

        # Συμβουλές
        report.append("💡 ΣΥΜΒΟΥΛΕΣ ΒΕΛΤΙΩΣΗΣ:")

        if self.analysis_results['mean_paradox'] > 30:
            report.append("  1. ΑΥΞΗΜΕΝΗ ΠΑΡΑΔΟΞΟΤΗΤΑ: Το μοντέλο τείνει προς ταυτόχρονες ακραίες καταστάσεις.")
            report.append("     • Εξετάστε διαφορετική αρχιτεκτονική (π.χ., GRU αντί για LSTM)")
            report.append("     • Προσθέστε batch normalization")
            report.append("     • Χρησιμοποιήστε διαφορετικό activation function (π.χ., swish)")

        if len(self.analysis_results['high_risk_steps']) > self.timesteps / 3:
            report.append("  2. ΠΟΛΛΑΠΛΟΙ ΚΙΝΔΥΝΟΙ: Πολλά βήματα σε κίνδυνο ποιοτικής αλλαγής.")
            report.append("     • Αυξήστε το dropout rate")
            report.append("     • Προσθέστε L2 regularization")
            report.append("     • Μειώστε το learning rate")

        if self.analysis_results['mean_false_stab'] > 40:
            report.append("  3. ΨΕΥΔΗΣ ΣΤΑΘΕΡΟΤΗΤΑ: Η 'σταθερότητα' κρύβει αντιφάσεις.")
            report.append("     • Προσθέστε Gaussian noise στα training data")
            report.append("     • Χρησιμοποιήστε mixup augmentation")
            report.append("     • Εφαρμόστε stochastic depth")

        if not (self.analysis_results['mean_paradox'] > 30 or
                len(self.analysis_results['high_risk_steps']) > self.timesteps / 3 or
                self.analysis_results['mean_false_stab'] > 40):
            report.append("  ✅ Το μοντέλο έχει υγιή διαλεκτική συμπεριφορά.")
            report.append("     • Συνεχίστε την τρέχουσα προσέγγιση")
            report.append("     • Παρακολουθήστε περιοδικά για τυχόν αλλαγές")

        report.append("")
        report.append("="*70)
        report.append("ΤΕΛΟΣ ΑΝΑΛΥΣΗΣ")
        report.append("="*70)

        return "\n".join(report)

# ============================================
# ΕΚΚΙΝΗΣΗ ΤΟΥ ΔΙΑΔΡΑΣΤΙΚΟΥ ΑΝΑΛΥΤΗ
# ============================================

print("\n" + "="*70)
print("🎯 ΔΙΑΔΡΑΣΤΙΚΟΣ ΑΝΑΛΥΤΗΣ LSTM ΜΕ ΞΕΝΟΠΟΥΛΟ")
print("="*70)
print("\nΟδηγίες χρήσης:")
print("1. Ρυθμίστε τις παραμέτρους στα sliders")
print("2. Κάντε κλικ στο 'Εκπαίδευση & Ανάλυση'")
print("3. Περιμένετε την ολοκλήρωση (2-5 λεπτά)")
print("4. Κάντε κλικ στο 'Οπτικοποίηση Αποτελεσμάτων'")
print("5. Χρησιμοποιήστε το 'Εξαγωγή Αναφοράς' για να αποθηκεύσετε\n")

# Αρχικοποίηση του αναλυτή
analyzer = InteractiveXenopoulosAnalyzer()
