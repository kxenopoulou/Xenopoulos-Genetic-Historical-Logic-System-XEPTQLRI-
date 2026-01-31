
# ============================================================================
# ΑΝΑΛΥΣΗ ΚΩΔΙΚΑ ΜΕ ΤΟ ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ - GOOGLE COLAB ΕΚΔΟΧΗ
# ============================================================================

# 1. ΕΓΚΑΤΑΣΤΑΣΗ ΒΙΒΛΙΟΘΗΚΩΝ (τρέχει μόνο στο Colab)
!pip install numpy pandas matplotlib seaborn plotly -q

# 2. ΕΙΣΑΓΩΓΗ ΒΙΒΛΙΟΘΗΚΩΝ
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.style.use('default')
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [12, 8]

# 3. Ο ΚΩΔΙΚΑΣ ΣΟΥ - ΑΚΡΙΒΩΣ ΟΠΩΣ ΤΟΝ ΕΔΩΣΕΣ
def calculate_temperature_factor(temperature):
    if temperature > 250:
        return 1 + 0.7 * np.log1p(temperature - 250)
    return 1

def calculate_interaction_factor(interaction_type):
    return {"strong": 1.5, "weak": 1.2}.get(interaction_type, 1.0)

def calculate_frequency_factor(frequency):
    return 1 + 0.65 * np.log(frequency)

def calculate_general_type(noise_level, temperature, frequency, interaction_type):
    alpha = 1.2 / (1 + 1.5 * noise_level)
    beta = max(0.25, 1 - temperature / 450)
    
    k_T = calculate_temperature_factor(temperature)
    beta_interaction = calculate_interaction_factor(interaction_type)
    k_f = calculate_frequency_factor(frequency)
    
    gamma = alpha * (beta**0.8) * k_f
    result = alpha * gamma * (k_T * beta_interaction)**0.9
    
    return result

print("✅ Ο ΚΩΔΙΚΑΣ ΣΟΥ ΦΟΡΤΩΘΗΚΕ!")

# 4. ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ ΓΙΑ ΤΟΝ ΣΥΓΚΕΚΡΙΜΕΝΟ ΚΩΔΙΚΑ
class XenopoulosCodeAnalyzer:
    def __init__(self):
        self.history = []
        self.paradox_events = []
        
    def simulate_code_behavior(self, num_simulations=200):
        """Προσομοίωση πολλών εκτελέσεων του κώδικα"""
        results = []
        parameters = []
        
        np.random.seed(42)
        
        for i in range(num_simulations):
            # Τυχαίες είσοδοι (όπως στον πίνακα σύγκρισης)
            if i < num_simulations//3:
                # Δοκιμή 1: Μέτριες τιμές
                noise = 0.4  # 80% (μέτριος)
                temp = 150   # 70% (μέτρια)
                freq = 1000  # 50% (μέτρια)
                inter = "strong"  # 90% (ισχυρή)
            elif i < 2*num_simulations//3:
                # Δοκιμή 2: Καλές τιμές
                noise = 0.3  # 90% (χαμηλός)
                temp = 100   # 85% (ιδανική)
                freq = 2000  # 100% (υψηλή)
                inter = "strong"  # 100% (ισχυρή)
            else:
                # Δοκιμή 3: Βελτιωμένη
                noise = 0.2  # 100% (χαμηλός)
                temp = 300   # 75% (υψηλή, 3.75x)
                freq = 1500  # 90% (υψηλή, 5.75x)
                inter = "strong"  # 100% (ισχυρή, 1.50x)
            
            # Προσθήκη μικρής τυχαιότητας
            noise += np.random.uniform(-0.05, 0.05)
            temp += np.random.uniform(-10, 10)
            freq += np.random.uniform(-100, 100)
            
            # Εκτέλεση του ΚΩΔΙΚΑ ΣΟΥ
            result = calculate_general_type(noise, temp, freq, inter)
            
            results.append(result)
            parameters.append({
                'noise': noise,
                'temperature': temp,
                'frequency': freq,
                'interaction': inter,
                'test_group': 'Δοκιμή 1' if i < num_simulations//3 else 
                             ('Δοκιμή 2' if i < 2*num_simulations//3 else 'Δοκιμή 3')
            })
            
            # Διαλεκτική ανάλυση
            self._analyze_dialectically(result, parameters[-1], i)
        
        return results, parameters
    
    def _analyze_dialectically(self, result, params, step):
        """Διαλεκτική ανάλυση κάθε αποτελέσματος"""
        # Δημιουργία διαλεκτικού ζεύγους
        A = result  # Η "θέση" - το αποτέλεσμα
        not_A = -result * 0.85  # Η "αντίθεση" - διαλεκτική άρνηση
        
        # Υπολογισμός διαλεκτικής έντασης
        tension = abs(A * not_A)
        
        # Έλεγχος για παραδοξολογική υπέρβαση (Κριτήρια Ξενόπουλου)
        simultaneous_extremity = (abs(A) > 0.8) and (abs(not_A) > 0.8)
        low_tension = tension < 0.3
        is_paradoxical = simultaneous_extremity and low_tension
        
        # Αποθήκευση
        analysis = {
            'step': step,
            'A': A,
            'not_A': not_A,
            'tension': tension,
            'is_paradoxical': is_paradoxical,
            'params': params,
            'result': result
        }
        
        self.history.append(analysis)
        
        if is_paradoxical:
            self.paradox_events.append(analysis)
    
    def calculate_XEPTQLRI(self):
        """Υπολογισμός XEPTQLRI για όλη την ιστορία"""
        if len(self.history) < 5:
            return np.zeros(len(self.history))
        
        xeptqlri_values = []
        
        for i in range(len(self.history)):
            # Παράθυρο τελευταίων 5 τιμών
            window_start = max(0, i-4)
            window = self.history[window_start:i+1]
            
            # Διαλεκτική Ένταση (τυπική απόκλιση των Α)
            A_values = [h['A'] for h in window]
            dialectical_tension = np.std(A_values) if len(A_values) > 1 else 0.1
            
            # Ιστορική Τάση (κλίση)
            if len(window) > 1:
                x = np.arange(len(window))
                y = [h['result'] for h in window]
                slope = abs(np.polyfit(x, y, 1)[0])
                historical_trend = 1 + slope * 10
            else:
                historical_trend = 1.0
            
            # Παράγοντας Παραδόξου
            extreme_count = sum(1 for h in window if abs(h['A']) > 0.7)
            paradox_factor = extreme_count / len(window)
            
            # Όριο Aufhebung (σταθερό)
            aufhebung_threshold = 0.65
            
            # Τελικός XEPTQLRI
            xeptqlri = (dialectical_tension * historical_trend * paradox_factor) / aufhebung_threshold
            xeptqlri_values.append(xeptqlri)
        
        return xeptqlri_values
    
    def generate_report(self):
        """Δημιουργία αναφοράς ανάλυσης"""
        xeptqlri = self.calculate_XEPTQLRI()
        
        report = {
            'total_simulations': len(self.history),
            'paradox_count': len(self.paradox_events),
            'paradox_percentage': len(self.paradox_events) / len(self.history) * 100,
            'mean_result': np.mean([h['result'] for h in self.history]),
            'std_result': np.std([h['result'] for h in self.history]),
            'mean_tension': np.mean([h['tension'] for h in self.history]),
            'mean_xeptqlri': np.mean(xeptqlri) if xeptqlri else 0,
            'max_xeptqlri': np.max(xeptqlri) if xeptqlri else 0,
            'xeptqlri_values': xeptqlri,
            'paradox_events': self.paradox_events
        }
        
        return report

# 5. ΕΚΤΕΛΕΣΗ ΑΝΑΛΥΣΗΣ
print("🔍 ΕΚΤΕΛΩ ΑΝΑΛΥΣΗ ΤΟΥ ΚΩΔΙΚΑ ΣΟΥ ΜΕ ΤΟ ΣΥΣΤΗΜΑ ΞΕΝΟΠΟΥΛΟΥ...")

analyzer = XenopoulosCodeAnalyzer()
results, parameters = analyzer.simulate_code_behavior(300)
report = analyzer.generate_report()

print("\n" + "="*60)
print("📊 ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΛΥΣΗΣ")
print("="*60)
print(f"Σύνολο προσομοιώσεων: {report['total_simulations']}")
print(f"Παραδοξολογικές υπερβάσεις: {report['paradox_count']} ({report['paradox_percentage']:.1f}%)")
print(f"Μέση τιμή αποτελέσματος: {report['mean_result']:.3f}")
print(f"Μέση διαλεκτική ένταση: {report['mean_tension']:.3f}")
print(f"Μέσος XEPTQLRI: {report['mean_xeptqlri']:.3f}")
print(f"Μέγιστος XEPTQLRI: {report['max_xeptqlri']:.3f}")

if report['paradox_count'] > 0:
    print(f"\n⚠️  ΕΝΤΟΠΙΣΘΗΚΑΝ {report['paradox_count']} ΠΑΡΑΔΟΞΟΛΟΓΙΚΕΣ ΥΠΕΡΒΑΣΕΙΣ!")
    print("   Αυτό σημαίνει ότι ο κώδικας σου λειτουργεί σε καταστάσεις")
    print("   'ψευδούς σταθερότητας' σύμφωνα με το Σύστημα Ξενόπουλου!")

# 6. ΔΙΑΓΡΑΜΜΑ 1: ΧΡΟΝΟΣΕΙΡΑ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ΚΑΙ XEPTQLRI
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# 6.1 Χρονοσειρά αποτελέσματα
ax1 = axes[0]
steps = np.arange(len(results))
ax1.plot(steps, results, 'b-', alpha=0.7, linewidth=1.5, label='Αποτέλεσμα')
ax1.fill_between(steps, results, alpha=0.2, color='blue')

# Χρωματικές περιοχές για τις 3 δοκιμές
test1_end = len(results)//3
test2_end = 2*len(results)//3
ax1.axvspan(0, test1_end, alpha=0.1, color='red', label='Δοκιμή 1')
ax1.axvspan(test1_end, test2_end, alpha=0.1, color='green', label='Δοκιμή 2')
ax1.axvspan(test2_end, len(results), alpha=0.1, color='orange', label='Δοκιμή 3')

# Σημεία παραδόξου
paradox_steps = [h['step'] for h in analyzer.paradox_events]
paradox_results = [h['result'] for h in analyzer.paradox_events]
if paradox_steps:
    ax1.scatter(paradox_steps, paradox_results, color='black', s=100, 
                zorder=5, label=f'Παραδοξολογική Υπέρβαση ({len(paradox_steps)})')

ax1.set_title('ΑΝΑΛΥΣΗ ΚΩΔΙΚΑ: Χρονοσειρά Αποτελεσμάτων', fontsize=14, fontweight='bold')
ax1.set_xlabel('Αριθμός Προσομοίωσης')
ax1.set_ylabel('Τιμή Αποτελέσματος')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# 6.2 XEPTQLRI
ax2 = axes[1]
xeptqlri = report['xeptqlri_values']
ax2.plot(steps, xeptqlri, color='darkorange', linewidth=2, label='Δείκτης XEPTQLRI')
ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Όριο Χαμηλού Κινδύνου (0.5)')

# Χρωματικές περιοχές κινδύνου
ax2.fill_between(steps, 0, 0.5, alpha=0.2, color='green', label='Χαμηλός Κίνδυνος')
ax2.fill_between(steps, 0.5, max(xeptqlri)*1.1, alpha=0.2, color='orange', label='Μέσος/Υψηλός Κίνδυνος')

# Σημεία παραδόξου στο XEPTQLRI
if paradox_steps:
    ax2.scatter(paradox_steps, [xeptqlri[s] for s in paradox_steps], 
               color='black', s=100, zorder=5, label='Παράδοξο')

ax2.set_title('ΔΕΙΚΤΗΣ XEPTQLRI - Ανίχνευση Κρυφών Κινδύνων', fontsize=14, fontweight='bold')
ax2.set_xlabel('Αριθμός Προσομοίωσης')
ax2.set_ylabel('Τιμή XEPTQLRI')
ax2.legend(loc='upper left')
ax2.set_ylim(0, max(xeptqlri)*1.1)
ax2.grid(True, alpha=0.3)

# 6.3 Διαλεκτική Ένταση και Παράδοξο
ax3 = axes[2]

# Διαλεκτική ένταση
tension_values = [h['tension'] for h in analyzer.history]
ax3.plot(steps, tension_values, color='green', linewidth=2, label='Διαλεκτική Ένταση')

# Παράγοντας Παραδόξου (κυλιόμενος)
paradox_window = 10
paradox_rolling = []
for i in range(len(analyzer.history)):
    window_start = max(0, i - paradox_window + 1)
    window = analyzer.history[window_start:i+1]
    paradox_count = sum(1 for h in window if h['is_paradoxical'])
    paradox_rolling.append(paradox_count / len(window))
    
ax3.plot(steps, paradox_rolling, color='red', linewidth=2, label='Παράγοντας Παραδόξου (Κυλιόμενος)')

# Ορίζοντες γραμμές
ax3.axhline(y=0.3, color='orange', linestyle=':', alpha=0.7, label='Όριο Χαμηλής Έντασης (0.3)')
ax3.axhline(y=0.5, color='purple', linestyle=':', alpha=0.7, label='Όριο Υψηλού Παράγοντα (0.5)')

# Σημεία παραδόξου
for step in paradox_steps:
    ax3.axvline(x=step, color='red', alpha=0.3, linewidth=0.5)

ax3.set_title('ΔΙΑΛΕΚΤΙΚΗ ΔΥΝΑΜΙΚΗ - Ένταση vs Παράδοξο', fontsize=14, fontweight='bold')
ax3.set_xlabel('Αριθμός Προσομοίωσης')
ax3.set_ylabel('Τιμές')
ax3.legend(loc='upper left')
ax3.set_ylim(0, 1)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kodikas_xenopoulos_analysis_1.png', dpi=150, bbox_inches='tight')
plt.show()

# 7. ΔΙΑΓΡΑΜΜΑ 2: ΧΑΡΤΗΣ ΦΑΣΕΩΝ ΚΑΙ ΣΤΑΤΙΣΤΙΚΗ ΑΝΑΛΥΣΗ
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 7.1 Χάρτης Φάσεων (A vs ¬A)
ax1 = axes[0, 0]
A_values = [h['A'] for h in analyzer.history]
not_A_values = [h['not_A'] for h in analyzer.history]

# Χρωματισμός βάσει δοκιμής
colors = []
for h in analyzer.history:
    if h['step'] < test1_end:
        colors.append('red')
    elif h['step'] < test2_end:
        colors.append('green')
    else:
        colors.append('orange')

scatter = ax1.scatter(A_values, not_A_values, c=colors, alpha=0.6, s=30)

# Περιοχή παραδόξου
paradox_A = [h['A'] for h in analyzer.paradox_events]
paradox_not_A = [h['not_A'] for h in analyzer.paradox_events]
if paradox_A:
    ax1.scatter(paradox_A, paradox_not_A, color='black', s=100, 
                marker='X', label='Παραδοξολογική Υπέρβαση')

# Γραμμές και περιοχές
ax1.axhline(y=0, color='gray', alpha=0.3, linewidth=0.5)
ax1.axvline(x=0, color='gray', alpha=0.3, linewidth=0.5)
ax1.axhline(y=0.8, color='red', linestyle='--', alpha=0.5, linewidth=0.8)
ax1.axhline(y=-0.8, color='red', linestyle='--', alpha=0.5, linewidth=0.8)
ax1.axvline(x=0.8, color='red', linestyle='--', alpha=0.5, linewidth=0.8)
ax1.axvline(x=-0.8, color='red', linestyle='--', alpha=0.5, linewidth=0.8)

ax1.set_title('ΧΑΡΤΗΣ ΦΑΣΕΩΝ: A vs ¬A', fontsize=13, fontweight='bold')
ax1.set_xlabel('Κατάσταση A (Θέση)')
ax1.set_ylabel('Κατάσταση ¬A (Αντίθεση)')
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.grid(True, alpha=0.2)
ax1.legend()

# 7.2 Ιστογράμματα κατανομής
ax2 = axes[0, 1]
ax2.hist(A_values, bins=30, alpha=0.5, color='blue', label='Κατανομή A', density=True)
ax2.hist(not_A_values, bins=30, alpha=0.5, color='red', label='Κατανομή ¬A', density=True)

# KDE
from scipy.stats import gaussian_kde
kde_A = gaussian_kde(A_values)
kde_not_A = gaussian_kde(not_A_values)
x_range = np.linspace(-1.5, 1.5, 200)
ax2.plot(x_range, kde_A(x_range), 'b-', linewidth=2)
ax2.plot(x_range, kde_not_A(x_range), 'r-', linewidth=2)

ax2.axvline(x=0.8, color='red', linestyle='--', alpha=0.7, label='Όριο Παραδόξου')
ax2.axvline(x=-0.8, color='red', linestyle='--', alpha=0.7)

ax2.set_title('ΚΑΤΑΝΟΜΗ ΔΙΑΛΕΚΤΙΚΩΝ ΜΕΤΑΒΛΗΤΩΝ', fontsize=13, fontweight='bold')
ax2.set_xlabel('Τιμή')
ax2.set_ylabel('Πυκνότητα Πιθανότητας')
ax2.legend()
ax2.grid(True, alpha=0.2)

# 7.3 Ανάλυση ανά Δοκιμή
ax3 = axes[1, 0]

test_groups = ['Δοκιμή 1', 'Δοκιμή 2', 'Δοκιμή 3']
test_results = [[], [], []]
test_xeptqlri = [[], [], []]

for i, h in enumerate(analyzer.history):
    group_idx = 0 if i < test1_end else (1 if i < test2_end else 2)
    test_results[group_idx].append(h['result'])
    test_xeptqlri[group_idx].append(report['xeptqlri_values'][i])

# Box plot αποτελεσμάτων
box_data = []
for group in test_results:
    if group:  # Ελέγχουμε αν η λίστα δεν είναι άδεια
        box_data.append(group)

bp = ax3.boxplot(box_data, patch_artist=True)
colors = ['lightcoral', 'lightgreen', 'wheat']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Προσθήκη μέσων τιμών
for i, group in enumerate(test_results):
    if group:
        mean_val = np.mean(group)
        ax3.scatter(i+1, mean_val, color='black', s=100, zorder=5, marker='D')

ax3.set_title('ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑ ΔΟΚΙΜΗ (Box Plot)', fontsize=13, fontweight='bold')
ax3.set_xlabel('Ομάδα Δοκιμής')
ax3.set_ylabel('Τιμή Αποτελέσματος')
ax3.set_xticklabels(test_groups)
ax3.grid(True, alpha=0.2)

# 7.4 Ανάλυση Παραμέτρων
ax4 = axes[1, 1]

# Δεδομένα παραμέτρων ανά δοκιμή
param_names = ['Θόρυβος', 'Θερμοκρασία', 'Συχνότητα']
param_values = np.array([
    [0.4, 150, 1000],   # Δοκιμή 1
    [0.3, 100, 2000],   # Δοκιμή 2
    [0.2, 300, 1500]    # Δοκιμή 3
])

# Κλιμάκωση για καλύτερη οπτικοποίηση
param_scaled = param_values.copy()
param_scaled[:, 0] *= 10  # Θόρυβος x10
param_scaled[:, 1] /= 50  # Θερμοκρασία /50
param_scaled[:, 2] /= 200 # Συχνότητα /200

x = np.arange(len(param_names))
width = 0.25

bars1 = ax4.bar(x - width, param_scaled[0], width, label='Δοκιμή 1', color='lightcoral')
bars2 = ax4.bar(x, param_scaled[1], width, label='Δοκιμή 2', color='lightgreen')
bars3 = ax4.bar(x + width, param_scaled[2], width, label='Δοκιμή 3', color='wheat')

ax4.set_title('ΤΙΜΕΣ ΠΑΡΑΜΕΤΡΩΝ ΑΝΑ ΔΟΚΙΜΗ', fontsize=13, fontweight='bold')
ax4.set_xlabel('Παράμετρος')
ax4.set_ylabel('Κλιμακωμένη Τιμή')
ax4.set_xticks(x)
ax4.set_xticklabels(param_names)
ax4.legend()
ax4.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('kodikas_xenopoulos_analysis_2.png', dpi=150, bbox_inches='tight')
plt.show()

# 8. ΤΕΛΙΚΗ ΑΝΑΛΥΤΙΚΗ ΕΚΘΕΣΗ
print("\n" + "="*70)
print("🎯 ΤΕΛΙΚΗ ΔΙΑΓΝΩΣΗ ΓΙΑ ΤΟΝ ΚΩΔΙΚΑ ΣΟΥ")
print("="*70)

print(f"\n📋 ΒΑΣΙΚΗ ΑΝΑΛΥΣΗ:")
print(f"   • Συνολικές προσομοιώσεις: {report['total_simulations']}")
print(f"   • Μέση τιμή αποτελέσματος: {report['mean_result']:.4f}")
print(f"   • Τυπική απόκλιση: {report['std_result']:.4f}")

print(f"\n⚠️  ΑΝΑΛΥΣΗ ΚΙΝΔΥΝΩΝ ΞΕΝΟΠΟΥΛΟΥ:")
print(f"   • Παραδοξολογικές υπερβάσεις: {report['paradox_count']} ({report['paradox_percentage']:.1f}%)")
print(f"   • Μέση διαλεκτική ένταση: {report['mean_tension']:.3f}")
print(f"   • Μέσος XEPTQLRI: {report['mean_xeptqlri']:.3f}")

print(f"\n🔍 ΕΡΜΗΝΕΙΑ ΑΠΟΤΕΛΕΣΜΑΤΩΝ:")
if report['paradox_count'] == 0:
    print(f"   ✅ Ο κώδικας ΔΕΝ εμφανίζει παραδοξολογική συμπεριφορά")
    print(f"     Σύμφωνα με το Σύστημα Ξενόπουλου, αυτό είναι καλό σημάδι.")
else:
    print(f"   ⚠️  Ο κώδικας εμφανίζει {report['paradox_count']} περιπτώσεις")
    print(f"     παραδοξολογικής υπέρβασης.")
    print(f"     Αυτό σημαίνει ότι σε κάποιες συνθήκες, το σύστημα:")
    print(f"     - Φαίνεται σταθερό (χαμηλή διαλεκτική ένταση)")
    print(f"     - Αλλά έχει ακραίες τιμές (|A| > 0.8 και |¬A| > 0.8)")
    print(f"     - Υπάρχει κίνδυνος 'ψευδούς σταθερότητας'")

print(f"\n📈 ΣΥΓΚΡΙΣΗ ΔΟΚΙΜΩΝ:")
print(f"   • Δοκιμή 1 (Μέτριες παράμετροι):")
print(f"     - Θόρυβος: 80% | Θερμοκρασία: 70% | Συχνότητα: 50%")
print(f"     - Αποτέλεσμα: ~88.5% (σύμφωνα με τον πίνακα σου)")

print(f"   • Δοκιμή 2 (Καλές παράμετροι):")
print(f"     - Θόρυβος: 90% | Θερμοκρασία: 85% | Συχνότητα: 100%")
print(f"     - Αποτέλεσμα: ~96.3% (σύμφωνα με τον πίνακα σου)")

print(f"   • Δοκιμή 3 (Βελτιωμένες παράμετροι):")
print(f"     - Θόρυβος: 100% | Θερμοκρασία: 75% (3.75x) | Συχνότητα: 90% (5.75x)")
print(f"     - Αποτέλεσμα: ~97.5% (σύμφωνα με τον πίνακα σου)")

print(f"\n💡 ΠΡΟΤΑΣΕΙΣ ΒΑΣΕΙ ΤΗΣ ΑΝΑΛΥΣΗΣ:")
if report['paradox_count'] > 0:
    print(f"   1. Προσθήκη ελέγχου για ταυτόχρονη ακραία τιμή A και ¬A")
    print(f"   2. Εισαγωγή 'διαλεκτικού ελέγχου' όπου |A| > 0.8 και |¬A| > 0.8")
    print(f"   3. Καταγραφή των συνθηκών που οδηγούν σε παραδοξολογική υπέρβαση")
else:
    print(f"   1. Ο κώδικας είναι διαλεκτικά υγιής")
    print(f"   2. Συνεχίστε με την τρέχουσα προσέγγιση")

print(f"\n📁 ΑΡΧΕΙΑ ΔΙΑΓΡΑΜΜΑΤΩΝ:")
print(f"   ✅ kodikas_xenopoulos_analysis_1.png - Χρονοσειρές και δείκτες")
print(f"   ✅ kodikas_xenopoulos_analysis_2.png - Χάρτες και στατιστικά")

print("\n" + "="*70)
print("✅ Η ΑΝΑΛΥΣΗ ΤΟΥ ΣΥΓΚΕΚΡΙΜΕΝΟΥ ΚΩΔΙΚΑ ΣΟΥ ΟΛΟΚΛΗΡΩΘΗΚΕ!")
print("="*70)
