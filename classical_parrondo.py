import numpy as np
import matplotlib.pyplot as plt
import itertools
import math

# ==========================================
# 1. ΒΑΣΙΚΕΣ ΠΑΡΑΜΕΤΡΟΙ ΠΙΘΑΝΟΤΗΤΩΝ
# ==========================================
epsilon = 0.005
base_pA = 0.5
base_pB1 = 0.10  
base_pB2 = 0.75  

n_trials = 100000 
initial_capital = 16

# ==========================================
# 2. ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ ΣΥΝΔΥΑΣΜΩΝ ΟΛΩΝ ΤΩΝ ΜΗΚΩΝ
# ==========================================
max_sequence_length = 10

games = ['A', 'B']
sequences_to_test = ["BBAABABABB"]
#sequences_to_test = []
#
#for length in range(1, max_sequence_length + 1):
 #   for p in itertools.product(games, repeat=length):
  #      sequences_to_test.append(''.join(p))

# ==========================================
# 3. ΜΗΧΑΝΙΣΜΟΣ ΠΑΙΓΝΙΩΝ 
# ==========================================
def play_A():
    return 1 if np.random.random() < (base_pA - epsilon) else -1

def play_B(capital):
    if capital % 3 == 0:
        p_win = base_pB1 - epsilon
    else:
        p_win = base_pB2 - epsilon
    return 1 if np.random.random() < p_win else -1

def play_sequence(sequence_str):
    capital = initial_capital
    steps = len(sequence_str) 
    
    for step in range(steps):
        current_game = sequence_str[step]
        if current_game == 'A':
            capital += play_A()
        elif current_game == 'B':
            capital += play_B(capital)
    return capital

# ==========================================
# 4. ΕΚΤΕΛΕΣΗ ΚΑΙ ΣΥΛΛΟΓΗ ΔΕΔΟΜΕΝΩΝ
# ==========================================
print(f"--- ΕΝΑΡΞΗ ΠΡΟΣΟΜΟΙΩΣΗΣ ---")
print(f"Μέγιστο Μήκος: {max_sequence_length}")
print(f"Δημιουργήθηκαν {len(sequences_to_test)} συνδυασμοί.")
print("-" * 40)

results = {}

for seq in sequences_to_test:
    final_capitals = np.zeros(n_trials)
    for i in range(n_trials):
        final_capitals[i] = play_sequence(seq)
    results[seq] = final_capitals

# ==========================================
# 5. ΕΚΤΥΠΩΣΗ ΑΚΡΙΒΩΝ ΠΙΘΑΝΟΤΗΤΩΝ
# ==========================================
for seq, data in results.items():
    actual_steps = len(seq)
    print(f"\n[ ΠΑΙΧΝΙΔΙ: {seq} ] -> Συνολικά Βήματα: {actual_steps}")
    mean_val = np.mean(data)
    print(f"Μέσο Τελικό Κεφάλαιο: {mean_val:.2f}")
    
    unique_capitals, counts = np.unique(data, return_counts=True)
    probabilities = (counts / n_trials) * 100
    
    sorted_indices = np.argsort(-probabilities)
    for i in range(min(5, len(unique_capitals))):
        idx = sorted_indices[i]
        print(f" -> Πιθανότητα για κεφάλαιο {unique_capitals[idx]:.0f}: {probabilities[idx]:.2f}%")

# ==========================================
# 6. ΔΗΜΙΟΥΡΓΙΑ ΤΩΝ ΔΙΑΓΡΑΜΜΑΤΩΝ (Ανά 4 ανά παράθυρο)
# ==========================================
items = list(results.items())
plots_per_window = 4
n_seq = len(items)
colors = plt.cm.plasma(np.linspace(0, 0.8, n_seq))
windows_opened=0
# Σπάμε τη λίστα των αποτελεσμάτων σε ομάδες των 4
start_index = 0  # Ξεκινάει κατευθείαν από τη σελίδα 341
for i in range(start_index, n_seq, plots_per_window):
    chunk = items[i:i + plots_per_window]
    
    # Φτιάχνουμε νέο παράθυρο 2x2 για την τρέχουσα τετράδα
    fig, axes = plt.subplots(2, 2, figsize=(15, 8))
    axes = axes.flatten()
    
    for j, (seq, data) in enumerate(chunk):
        ax = axes[j]
        actual_steps = len(seq)
        global_idx = i + j  
        
        unique_capitals, counts = np.unique(data, return_counts=True)
        probs = (counts / n_trials) * 100  # Μετατροπή σε ποσοστό %
        
        # 1. Αποθηκεύουμε το ραβδόγραμμα στη μεταβλητή 'bars'
        bars = ax.bar(unique_capitals, probs, color=colors[global_idx], edgecolor='black', alpha=0.8)
        
        # 2. ΠΡΟΣΘΗΚΗ: Βάζουμε το ποσοστό ακριβώς πάνω από κάθε μπάρα (2 δεκαδικά)
        ax.bar_label(bars, fmt='%.2f%%', padding=3, fontsize=10, fontweight='bold')
        
        # Επέκταση του άξονα Y για να χωράνε άνετα τα ποσοστά και το Legend!
        ax.set_ylim(0, max(probs) + 15)
        
        # --- ΔΙΑΤΗΡΗΣΗ ΑΛΛΑΓΗΣ 3 (Η κόκκινη γραμμή, ο τίτλος και το legend παραμένουν ως είχαν) ---
        #mean_val = np.mean(data)
        #ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Μέσο: {mean_val:.2f}')
        
        ax.set_title(f'Sequence: {seq} (Steps: {actual_steps})', fontsize=12, fontweight='bold')
        ax.set_xlabel('Payoff', fontsize=10)
        ax.set_ylabel('Probability (%)', fontsize=10)
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        #ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.6)
    
    # Αν η τελευταία ομάδα έχει λιγότερα από 4 γραφήματα, διαγράφουμε τα κενά κουτάκια
    for j in range(len(chunk), plots_per_window):
        fig.delaxes(axes[j])
        
    page_num = (i // plots_per_window) + 1
    total_pages = (n_seq + plots_per_window - 1) // plots_per_window
    plt.suptitle(f"Κατανομές Parrondo - Σελίδα {page_num} από {total_pages}", fontsize=14, fontweight='bold')
    plt.tight_layout()

    windows_opened += 1
    if windows_opened == 4:  # Θα ανοίξει ΜΟΝΟ 10 παράθυρα (δηλαδή 40 γραφήματα) και θα σταματήσει
        break

# Εμφάνιση όλων των παραθύρων ταυτόχρονα
plt.show()