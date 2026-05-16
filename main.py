import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import sympy
import math
import hashlib
import time

class ElGamalCryptosystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🔷 ELGAMAL CRYPTOSYSTEM | PROBABILISTIC ENCRYPTION 🔷")
        self.root.geometry("1400x950")
        self.root.configure(bg='#0a1a1a')  # Dark teal theme
        
        # Research theme colors
        self.bg_color = "#0a1a1a"
        self.research_blue = "#00d4ff"
        self.research_teal = "#00ffcc"
        self.random_purple = "#9b59b6"
        self.success_green = "#2ecc71"
        
        # ElGamal parameters
        self.p = None
        self.g = None
        self.x = None
        self.y = None
        self.private_key = None
        self.public_key = None
        
        self.setup_ui()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_research_header(main_container)
        
        # Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('ElGamal.TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('ElGamal.TNotebook.Tab', background='#0d2a2a', foreground=self.research_teal,
                       padding=[15, 8], font=('Segoe UI', 10, 'bold'))
        style.map('ElGamal.TNotebook.Tab',
                 background=[('selected', self.research_teal), ('active', '#1a3a3a')],
                 foreground=[('selected', '#0a1a1a'), ('active', self.research_teal)])
        
        notebook = ttk.Notebook(main_container, style='ElGamal.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab1 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab1, text="🔷 ELGAMAL CORE")
        self.setup_elgamal_core()
        
        self.tab2 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab2, text="🎲 PROBABILISTIC ENCRYPTION")
        self.setup_probabilistic()
        
        self.tab3 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab3, text="🔓 MALLEABILITY ATTACK")
        self.setup_malleability()
        
        self.tab4 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(self.tab4, text="📊 RSA vs ElGamal")
        self.setup_comparison()
        
        self.create_status_bar(main_container)
    
    def create_research_header(self, parent):
        header = tk.Frame(parent, bg=self.bg_color, height=90)
        header.pack(fill=tk.X, pady=(10, 0))
        
        header_text = """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║  ███████╗██╗  ██████╗     █████╗ ███╗   ███╗ █████╗ ██╗     ███████╗██╗                 ║
║  ██╔════╝██║ ██╔════╝    ██╔══██╗████╗ ████║██╔══██╗██║     ██╔════╝██║                 ║
║  █████╗  ██║ ██║  ███╗    ███████║██╔████╔██║███████║██║     █████╗  ██║                 ║
║  ██╔══╝  ██║ ██║   ██║    ██╔══██║██║╚██╔╝██║██╔══██║██║     ██╔══╝  ██║                 ║
║  ███████╗██║╚██████╔╝    ██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗███████╗            ║
║  ╚══════╝╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝            ║
║                    TAHR ELGAMAL CRYPTOSYSTEM - 1985                                   ║
║              PROBABILISTIC ENCRYPTION · SEMANTIC SECURITY · DISCRETE LOGS              ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝
"""
        lbl = tk.Label(header, text=header_text, font=('Courier', 7), fg=self.research_teal,
                      bg=self.bg_color, justify=tk.LEFT)
        lbl.pack()
    
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg='#0d2a2a', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="🔷 ELGAMAL CRYPTOSYSTEM READY | PROBABILISTIC MODE",
                                     font=('Segoe UI', 9), fg=self.research_teal, bg='#0d2a2a')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        for _ in range(3):
            sym = tk.Label(status_frame, text="◈", font=('Arial', 10), fg=self.research_blue, bg='#0d2a2a')
            sym.pack(side=tk.RIGHT, padx=5)
    
    # ==================== ELGAMAL CORE FUNCTIONS ====================
    def generate_prime(self, bits=512):
        """Generate a prime number with specified bits"""
        return sympy.randprime(2**(bits-1), 2**bits)
    
    def find_primitive_root(self, p):
        """Find a primitive root modulo p"""
        if p == 2:
            return 1
        
        # Factorize p-1
        factors = sympy.factorint(p-1)
        
        for g in range(2, min(p, 100)):  # Search up to 100
            valid = True
            for factor in factors.keys():
                if pow(g, (p-1)//factor, p) == 1:
                    valid = False
                    break
            if valid:
                return g
        return 2  # Fallback
    
    def generate_keypair(self, bits=512):
        """Generate ElGamal key pair"""
        self.p = self.generate_prime(bits)
        self.g = self.find_primitive_root(self.p)
        self.x = random.randint(2, self.p-2)  # private key
        self.y = pow(self.g, self.x, self.p)   # public key
        
        self.private_key = self.x
        self.public_key = (self.p, self.g, self.y)
        
        return self.public_key, self.private_key
    
    def encrypt(self, message, public_key=None):
        """Encrypt a message using ElGamal"""
        if public_key is None:
            public_key = self.public_key
        
        p, g, y = public_key
        
        # Choose random k
        k = random.randint(2, p-2)
        
        # Compute ciphertext
        c1 = pow(g, k, p)
        c2 = (message * pow(y, k, p)) % p
        
        return (c1, c2, k)  # k returned for demonstration only (not sent)
    
    def decrypt(self, ciphertext, private_key=None):
        """Decrypt a ciphertext using ElGamal"""
        if private_key is None:
            private_key = self.private_key
        
        c1, c2 = ciphertext[:2]
        p = self.p
        
        # Compute shared secret
        s = pow(c1, private_key, p)
        s_inv = pow(s, p-2, p)  # Modular inverse
        
        # Recover message
        message = (c2 * s_inv) % p
        
        return message
    
    # ==================== TAB 1: ELGAMAL CORE ====================
    def setup_elgamal_core(self):
        main_frame = tk.Frame(self.tab1, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Control panel
        control_frame = tk.LabelFrame(main_frame, text="🔑 KEY GENERATION", 
                                      font=('Segoe UI', 11, 'bold'),
                                      fg=self.research_teal, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        control_frame.pack(fill=tk.X, pady=10)
        
        size_frame = tk.Frame(control_frame, bg=self.bg_color)
        size_frame.pack(pady=10)
        
        tk.Label(size_frame, text="Prime Size (bits):", font=('Segoe UI', 10),
                fg=self.research_teal, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.key_bits = ttk.Combobox(size_frame, values=["512", "1024", "2048"], width=10)
        self.key_bits.set("512")
        self.key_bits.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="🔑 GENERATE ELGAMAL KEY PAIR", command=self.generate_elgamal_keys,
                 font=('Segoe UI', 10, 'bold'), bg=self.research_blue, fg='#0a1a1a', padx=15).pack(pady=5)
        
        # Message input
        msg_frame = tk.LabelFrame(main_frame, text="📝 MESSAGE (integer M < p)", 
                                  font=('Segoe UI', 11, 'bold'),
                                  fg=self.research_teal, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        msg_frame.pack(fill=tk.X, pady=10)
        
        self.message_int = tk.Entry(msg_frame, width=30, font=('Consolas', 11),
                                    bg='#0d2a2a', fg='#00ff00')
        self.message_int.pack(pady=10)
        self.message_int.insert(0, "12345")
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="🔒 ENCRYPT", command=self.elgamal_encrypt,
                 font=('Segoe UI', 10, 'bold'), bg=self.research_blue, fg='#0a1a1a', padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔓 DECRYPT", command=self.elgamal_decrypt,
                 font=('Segoe UI', 10, 'bold'), bg=self.random_purple, fg='white', padx=15).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = tk.Frame(main_frame, bg=self.bg_color)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Keys display
        key_frame = tk.LabelFrame(results_frame, text="🔐 KEY INFORMATION", 
                                  font=('Segoe UI', 10, 'bold'),
                                  fg=self.research_teal, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        key_frame.pack(fill=tk.X, pady=5)
        
        self.key_text = scrolledtext.ScrolledText(key_frame, height=8, font=('Consolas', 9),
                                                  bg='#0d2a2a', fg='#00ff00')
        self.key_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Ciphertext display
        cipher_frame = tk.LabelFrame(results_frame, text="🔒 CIPHERTEXT (C1, C2)", 
                                     font=('Segoe UI', 10, 'bold'),
                                     fg=self.research_blue, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        cipher_frame.pack(fill=tk.X, pady=5)
        
        self.cipher_text = scrolledtext.ScrolledText(cipher_frame, height=4, font=('Consolas', 10),
                                                     bg='#0d2a2a', fg='#ffff00')
        self.cipher_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Decrypted result
        result_frame = tk.LabelFrame(results_frame, text="📄 DECRYPTED MESSAGE", 
                                     font=('Segoe UI', 10, 'bold'),
                                     fg=self.success_green, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        result_frame.pack(fill=tk.X, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=2, font=('Consolas', 11),
                                                     bg='#0d2a2a', fg='#00ff00')
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def generate_elgamal_keys(self):
        try:
            bits = int(self.key_bits.get())
            
            self.key_text.delete('1.0', tk.END)
            self.key_text.insert('1.0', f"🔑 Generating ElGamal-{bits} key pair...\n")
            self.root.update()
            
            start_time = time.time()
            public_key, private_key = self.generate_keypair(bits)
            gen_time = time.time() - start_time
            
            p, g, y = public_key
            
            self.key_text.insert(tk.END, f"✅ Key generation complete in {gen_time:.2f}s\n\n")
            self.key_text.insert(tk.END, f"PUBLIC KEY (p, g, y):\n")
            self.key_text.insert(tk.END, f"p = {p}\n")
            self.key_text.insert(tk.END, f"g = {g}\n")
            self.key_text.insert(tk.END, f"y = {y}\n\n")
            self.key_text.insert(tk.END, f"PRIVATE KEY (x):\n")
            self.key_text.insert(tk.END, f"x = {private_key}\n")
            self.key_text.insert(tk.END, f"p size: {p.bit_length()} bits\n")
            
            self.status_label.config(text=f"🔑 ElGamal-{bits} keys generated | p size: {p.bit_length()} bits")
            
        except Exception as e:
            messagebox.showerror("Error", f"Key generation failed: {str(e)}")
    
    def elgamal_encrypt(self):
        try:
            if self.p is None:
                messagebox.showerror("Error", "Generate keys first!")
                return
            
            message = int(self.message_int.get())
            
            if message >= self.p:
                messagebox.showerror("Error", f"Message must be less than p ({self.p})!")
                return
            
            # Encrypt
            c1, c2, k = self.encrypt(message)
            
            self.cipher_text.delete('1.0', tk.END)
            self.cipher_text.insert('1.0', f"🔒 ELGAMAL ENCRYPTION\n")
            self.cipher_text.insert(tk.END, "=" * 50 + "\n")
            self.cipher_text.insert(tk.END, f"Random k (ephemeral key): {k}\n")
            self.cipher_text.insert(tk.END, f"C1 = g^k mod p = {c1}\n")
            self.cipher_text.insert(tk.END, f"C2 = M * y^k mod p = {c2}\n")
            self.cipher_text.insert(tk.END, f"Ciphertext size: {(c1.bit_length() + c2.bit_length()) // 8} bytes\n")
            
            self.status_label.config(text="🔒 Encryption complete | Randomized ciphertext")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def elgamal_decrypt(self):
        try:
            if self.p is None:
                messagebox.showerror("Error", "Generate keys first!")
                return
            
            # Parse ciphertext from display
            text = self.cipher_text.get('1.0', tk.END)
            c1 = None
            c2 = None
            
            for line in text.split('\n'):
                if 'C1 =' in line:
                    c1 = int(line.split('=')[1].strip())
                if 'C2 =' in line:
                    c2 = int(line.split('=')[1].strip())
            
            if c1 is None or c2 is None:
                messagebox.showerror("Error", "No ciphertext to decrypt!")
                return
            
            # Decrypt
            decrypted = self.decrypt((c1, c2))
            
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', f"Decrypted message: {decrypted}\n")
            
            original = int(self.message_int.get())
            if decrypted == original:
                self.result_text.insert(tk.END, f"✅ Verification: D(E(M)) = M ({original == decrypted})")
                self.status_label.config(text="🔓 Decryption successful | Message recovered")
            else:
                self.result_text.insert(tk.END, f"❌ Verification failed!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    # ==================== TAB 2: PROBABILISTIC ENCRYPTION ====================
    def setup_probabilistic(self):
        main_frame = tk.Frame(self.tab2, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Description
        desc_frame = tk.LabelFrame(main_frame, text="🎲 PROBABILISTIC ENCRYPTION DEMONSTRATION", 
                                   font=('Segoe UI', 11, 'bold'),
                                   fg=self.research_teal, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        desc_frame.pack(fill=tk.X, pady=10)
        
        desc_text = """ElGamal is PROBABILISTIC: Same message encrypts to different ciphertexts each time!
        This provides semantic security - attackers cannot distinguish encrypted messages."""
        
        desc_lbl = tk.Label(desc_frame, text=desc_text, font=('Consolas', 10),
                           fg='#ffff00', bg=self.bg_color, wraplength=1400, justify=tk.LEFT)
        desc_lbl.pack(padx=10, pady=10)
        
        # Test control
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(control_frame, text="Message to encrypt:", font=('Segoe UI', 10),
                fg=self.research_teal, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.test_message = tk.Entry(control_frame, width=20, font=('Consolas', 10),
                                     bg='#0d2a2a', fg='#00ff00')
        self.test_message.insert(0, "12345")
        self.test_message.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="🎲 ENCRYPT 3 TIMES", command=self.demo_probabilistic,
                 font=('Segoe UI', 10, 'bold'), bg=self.random_purple, fg='white', padx=15).pack(side=tk.LEFT, padx=10)
        
        # Results
        results_frame = tk.LabelFrame(main_frame, text="📊 ENCRYPTION RESULTS (SAME MESSAGE)", 
                                      font=('Segoe UI', 11, 'bold'),
                                      fg=self.research_blue, bg=self.bg_color, relief=tk.GROOVE, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.prob_results = scrolledtext.ScrolledText(results_frame, height=20, font=('Consolas', 9),
                                                      bg='#0d2a2a', fg='#00ff00')
        self.prob_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def demo_probabilistic(self):
        try:
            if self.p is None:
                messagebox.showerror("Error", "Generate keys in ElGamal Core tab first!")
                return
            
            message = int(self.test_message.get())
            
            if message >= self.p:
                messagebox.showerror("Error", f"Message must be less than p ({self.p})!")
                return
            
            self.prob_results.delete('1.0', tk.END)
            self.prob_results.insert('1.0', "🎲 PROBABILISTIC ENCRYPTION DEMONSTRATION\n")
            self.prob_results.insert(tk.END, "=" * 70 + "\n\n")
            self.prob_results.insert(tk.END, f"Same message: {message}\n\n")
            
            encryptions = []
            
            for i in range(3):
                c1, c2, k = self.encrypt(message)
                encryptions.append((c1, c2, k))
                
                self.prob_results.insert(tk.END, f"Encryption #{i+1}:\n")
                self.prob_results.insert(tk.END, f"  Random k = {k}\n")
                self.prob_results.insert(tk.END, f"  C1 = {c1}\n")
                self.prob_results.insert(tk.END, f"  C2 = {c2}\n\n")
            
            # Check if all different
            unique_c1 = len(set(e[0] for e in encryptions))
            unique_c2 = len(set(e[1] for e in encryptions))
            
            self.prob_results.insert(tk.END, "📊 ANALYSIS:\n")
            self.prob_results.insert(tk.END, "-" * 50 + "\n")
            self.prob_results.insert(tk.END, f"Unique C1 values: {unique_c1}/3\n")
            self.prob_results.insert(tk.END, f"Unique C2 values: {unique_c2}/3\n\n")
            
            if unique_c1 == 3 and unique_c2 == 3:
                self.prob_results.insert(tk.END, "✅ All ciphertexts are DIFFERENT!\n")
                self.prob_results.insert(tk.END, "   This demonstrates probabilistic encryption.\n")
                self.prob_results.insert(tk.END, "   Semantic security prevents distinguishing encrypted messages.\n")
            else:
                self.prob_results.insert(tk.END, "⚠️ Some ciphertexts repeated (unlikely but possible)\n")
            
            self.status_label.config(text="🎲 Probabilistic encryption demonstrated | Different ciphertexts for same message")
            
        except Exception as e:
            messagebox.showerror("Error", f"Demo failed: {str(e)}")
    
    # ==================== TAB 3: MALLEABILITY ATTACK ====================
    def setup_malleability(self):
        main_frame = tk.Frame(self.tab3, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Description
        desc_frame = tk.LabelFrame(main_frame, text="🔓 MALLEABILITY ATTACK DEMONSTRATION", 
                                   font=('Segoe UI', 11, 'bold'),
                                   fg='#ff6b6b', bg=self.bg_color, relief=tk.GROOVE, bd=2)
        desc_frame.pack(fill=tk.X, pady=10)
        
        desc_text = """Malleability: Given ciphertext C = (C1, C2) for message M, attacker can create C' = (C1, 2·C2 mod p)
        which decrypts to 2M mod p - WITHOUT knowing the private key!"""
        
        desc_lbl = tk.Label(desc_frame, text=desc_text, font=('Consolas', 10),
                           fg='#ffff00', bg=self.bg_color, wraplength=1400, justify=tk.LEFT)
        desc_lbl.pack(padx=10, pady=10)
        
        # Test control
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(control_frame, text="🔓 DEMONSTRATE MALLEABILITY", command=self.demo_malleability,
                 font=('Segoe UI', 11, 'bold'), bg='#ff6b6b', fg='white', padx=15).pack()
        
        # Results
        results_frame = tk.LabelFrame(main_frame, text="📊 MALLEABILITY ATTACK RESULTS", 
                                      font=('Segoe UI', 11, 'bold'),
                                      fg='#ff6b6b', bg=self.bg_color, relief=tk.GROOVE, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.malleability_results = scrolledtext.ScrolledText(results_frame, height=20, font=('Consolas', 9),
                                                              bg='#0d2a2a', fg='#00ff00')
        self.malleability_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def demo_malleability(self):
        try:
            if self.p is None:
                messagebox.showerror("Error", "Generate keys in ElGamal Core tab first!")
                return
            
            original_message = 12345
            
            self.malleability_results.delete('1.0', tk.END)
            self.malleability_results.insert('1.0', "🔓 MALLEABILITY ATTACK DEMONSTRATION\n")
            self.malleability_results.insert(tk.END, "=" * 70 + "\n\n")
            
            # Encrypt original message
            c1, c2, k = self.encrypt(original_message)
            
            self.malleability_results.insert(tk.END, "📍 ORIGINAL CIPHERTEXT:\n")
            self.malleability_results.insert(tk.END, f"  Message M = {original_message}\n")
            self.malleability_results.insert(tk.END, f"  C1 = g^k mod p = {c1}\n")
            self.malleability_results.insert(tk.END, f"  C2 = M * y^k mod p = {c2}\n\n")
            
            # Forge ciphertext for 2M
            c2_forged = (2 * c2) % self.p
            forged_ciphertext = (c1, c2_forged)
            
            self.malleability_results.insert(tk.END, "📍 FORGED CIPHERTEXT (Attacker creates):\n")
            self.malleability_results.insert(tk.END, f"  Operation: C' = (C1, 2·C2 mod p)\n")
            self.malleability_results.insert(tk.END, f"  C1' = {c1} (unchanged)\n")
            self.malleability_results.insert(tk.END, f"  C2' = 2·{c2} mod p = {c2_forged}\n\n")
            
            # Decrypt forged ciphertext
            decrypted_forged = self.decrypt(forged_ciphertext)
            expected = (2 * original_message) % self.p
            
            self.malleability_results.insert(tk.END, "📍 DECRYPTION RESULTS:\n")
            self.malleability_results.insert(tk.END, f"  Forged ciphertext decrypts to: {decrypted_forged}\n")
            self.malleability_results.insert(tk.END, f"  Expected: 2·M mod p = {expected}\n\n")
            
            if decrypted_forged == expected:
                self.malleability_results.insert(tk.END, "✅ ATTACK SUCCESSFUL!\n")
                self.malleability_results.insert(tk.END, "  Mallory can multiply ciphertext by 2 without knowing the key!\n\n")
            else:
                self.malleability_results.insert(tk.END, "❌ Attack failed (unexpected)\n\n")
            
            self.malleability_results.insert(tk.END, "💡 IMPLICATIONS:\n")
            self.malleability_results.insert(tk.END, "  • ElGamal is MALLEABLE (not non-malleable)\n")
            self.malleability_results.insert(tk.END, "  • Attacker can manipulate ciphertext meaningfully\n")
            self.malleability_results.insert(tk.END, "  • Requires authenticated encryption in practice\n")
            self.malleability_results.insert(tk.END, "  • This is why we need MACs or digital signatures\n")
            
            self.status_label.config(text="🔓 Malleability demonstrated | Ciphertext can be manipulated without decryption")
            
        except Exception as e:
            messagebox.showerror("Error", f"Demonstration failed: {str(e)}")
    
    # ==================== TAB 4: RSA vs ElGamal ====================
    def setup_comparison(self):
        main_frame = tk.Frame(self.tab4, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        comparison_text = scrolledtext.ScrolledText(main_frame, height=35, font=('Consolas', 9),
                                                    bg='#0d2a2a', fg='#00ff00')
        comparison_text.pack(fill=tk.BOTH, expand=True)
        
        content = """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                    📊 RSA vs ElGamal - COMPREHENSIVE COMPARISON 📊                        ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

1. KEY & CIPHERTEXT SIZE COMPARISON (2048-bit security)
═══════════════════════════════════════════════════════════════════════════════════════════

┌──────────────┬──────────────┬──────────────┬─────────────────────────────────────────────┐
│ Parameter    │ RSA-2048     │ ElGamal-2048 │ Difference                                 │
├──────────────┼──────────────┼──────────────┼─────────────────────────────────────────────┤
│ Public Key   │ 256 bytes    │ 512 bytes    │ ElGamal 2x larger                         │
│ Private Key  │ 256 bytes    │ 256 bytes    │ Similar (but structure differs)           │
│ Ciphertext   │ 256 bytes    │ 512 bytes    │ ElGamal 2x larger!                        │
│ Key Gen Time │ ~0.5s        │ ~0.8s        │ ElGamal slightly slower                    │
└──────────────┴──────────────┴──────────────┴─────────────────────────────────────────────┘

WHY ELGAMAL HAS LARGER CIPHERTEXT:
───────────────────────────────────────────────────────────────────────────────────────────
ElGamal ciphertext = (C1, C2) where:
• C1 = g^k mod p  (p-bit number, ~256 bytes for 2048-bit p)
• C2 = M · y^k mod p  (p-bit number, ~256 bytes)

Total = 512 bytes (twice RSA's 256 bytes)

PRACTICAL IMPLICATIONS:
───────────────────────────────────────────────────────────────────────────────────────────
• More bandwidth required (2x network traffic)
• More storage needed (2x database size)
• Slower transmission for large messages
• Can be problematic for constrained environments

2. SECURITY PROPERTIES COMPARISON
═══════════════════════════════════════════════════════════════════════════════════════════

┌──────────────────────────┬──────────────────┬──────────────────┬─────────────────────────┐
│ Property                 │ RSA-OAEP         │ ElGamal          │ Winner                  │
├──────────────────────────┼──────────────────┼──────────────────┼─────────────────────────┤
│ Deterministic/Probabilistic│ Probabilistic   │ Probabilistic    │ Tie                     │
│ Semantic Security        │ Yes (with OAEP)  │ Yes              │ Tie                     │
│ Non-malleability         │ Yes (with OAEP)  │ NO!              │ RSA ✓                   │
│ IND-CCA2 Secure          │ Yes              │ No (in basic form)│ RSA ✓                   │
│ Forward Secrecy          │ No (without DHE) │ Yes (with ephemeral)│ ElGamal ✓            │
│ Quantum Resistance       │ No               │ No               │ Tie                     │
└──────────────────────────┴──────────────────┴──────────────────┴─────────────────────────┘

3. PERFORMANCE COMPARISON
═══════════════════════════════════════════════════════════════════════════════════════════

┌──────────────────────────┬──────────────────┬──────────────────┬─────────────────────────┐
│ Operation                │ RSA-2048         │ ElGamal-2048     │ Ratio                   │
├──────────────────────────┼──────────────────┼──────────────────┼─────────────────────────┤
│ Key Generation           │ 0.5s             │ 0.8s             │ ElGamal 1.6x slower     │
│ Encryption               │ 0.003s           │ 0.008s           │ ElGamal 2.7x slower     │
│ Decryption               │ 0.05s            │ 0.008s           │ ElGamal 6x FASTER!      │
│ Signature Generation     │ 0.05s            │ Not designed     │ N/A                     │
│ Signature Verification   │ 0.003s           │ Not designed     │ N/A                     │
└──────────────────────────┴──────────────────┴──────────────────┴─────────────────────────┘

Note: ElGamal decryption is much faster because it only requires one modular exponentiation!

4. PRACTICAL USE CASES
═══════════════════════════════════════════════════════════════════════════════════════════

RSA IS PREFERRED FOR:
───────────────────────────────────────────────────────────────────────────────────────────
• Digital signatures (PKCS#1, PSS)
• Key transport in TLS (though ECDHE is now preferred)
• Smart cards (smaller key sizes, faster encryption)
• Legacy systems with RSA hardware accelerators

ElGamal IS PREFERRED FOR:
───────────────────────────────────────────────────────────────────────────────────────────
• Systems requiring forward secrecy (when combined with ephemeral keys)
• Applications where decryption speed is critical
• Protocols that need probabilistic encryption natively
• Based on discrete logarithms (alternative security assumption)

5. MALLEABILITY: THE CRITICAL DIFFERENCE
═══════════════════════════════════════════════════════════════════════════════════════════

RSA WITH OAEP:
───────────────────────────────────────────────────────────────────────────────────────────
C = OAEP(M) ^ e mod n
Properties:
• Non-malleable (OAEP prevents manipulation)
• Any change to C results in random plaintext
• Chosen ciphertext secure

ElGamal (basic):
───────────────────────────────────────────────────────────────────────────────────────────
C = (g^k mod p, M·y^k mod p)
Properties:
• Malleable! (C1, C2) -> (C1, t·C2) decrypts to t·M
• Attacker can multiply ciphertext by any factor
• Requires additional authentication (MAC/signature)

SOLUTION FOR ELGAMAL:
───────────────────────────────────────────────────────────────────────────────────────────
Use ElGamal with DSA signature or combine with MAC:
C = (C1, C2, MAC(C1||C2))
This prevents tampering while preserving probabilistic nature

6. RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════════════════════════════

WHEN TO CHOOSE RSA:
───────────────────────────────────────────────────────────────────────────────────────────
✓ Need digital signatures
✓ Working with established standards (PKCS, TLS)
✓ Have hardware acceleration for RSA
✓ Need smaller ciphertext size

WHEN TO CHOOSE ElGamal:
───────────────────────────────────────────────────────────────────────────────────────────
✓ Need faster decryption
✓ Want probabilistic encryption natively
✓ Have bandwidth to spare (2x ciphertext)
✓ Can add authentication layer

BEST PRACTICE:
───────────────────────────────────────────────────────────────────────────────────────────
"Neither is perfect - use hybrid encryption with authenticated modes in practice!"

RECOMMENDATION FOR MODERN SYSTEMS:
───────────────────────────────────────────────────────────────────────────────────────────
• Use ECC (ECDH, ECDSA) instead of RSA or ElGamal
• Smaller keys, faster operations, same security
• Post-quantum cryptography coming (CRYSTALS-Kyber, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    🔷 ELGAMAL: PROBABILISTIC BUT MALLEABLE 🔷
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        comparison_text.insert('1.0', content)
        comparison_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = ElGamalCryptosystem(root)
    root.mainloop()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║              ELGAMAL CRYPTOSYSTEM - PROBABILISTIC ENCRYPTION          ║
    ║                                                                       ║
    ║     Features:                                                         ║
    ║     ✓ Full ElGamal implementation (prime generation, primitive root) ║
    ║     ✓ Probabilistic encryption demonstration                         ║
    ║     ✓ Malleability attack simulation                                 ║
    ║     ✓ RSA vs ElGamal comprehensive comparison                        ║
    ║     ✓ Semantic security analysis                                     ║
    ║                                                                       ║
    ║     Starting GUI...                                                  ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    main()