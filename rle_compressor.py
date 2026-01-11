import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
import wave
import os
import re

class RLECompressorApp:
    def __init__(self, root):
        # Ana pencereyi oluştur ve başlığı ayarla
        self.root = root
        self.root.title("Advanced RLE Compressor")
        self.root.geometry("1000x800")
        
        # Arayüz stillerini yapılandır
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        
        # Renk paleti tanımla
        self.colors = {
            'primary': '#4a7abc',
            'secondary': '#6c757d',
            'success': '#28a745',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
        # Widget'ları oluştur ve değişkenleri başlat
        self.create_widgets()
        self.current_file = None
        self.current_data_type = "text"
        
    def create_widgets(self):
        # Ana çerçeveyi oluştur ve yerleştir
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Veri türü seçim bölümü oluştur
        type_frame = ttk.LabelFrame(main_frame, text="Data Type", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.data_type = tk.StringVar(value="text")
        ttk.Radiobutton(type_frame, text="Text", variable=self.data_type, 
                       value="text", command=self.update_ui).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Image", variable=self.data_type, 
                       value="image", command=self.update_ui).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Audio", variable=self.data_type, 
                       value="audio", command=self.update_ui).pack(side=tk.LEFT, padx=10)
        
        # Input Frame
        self.input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        self.input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text input (default)
        self.text_input = scrolledtext.ScrolledText(self.input_frame, height=10, wrap=tk.WORD, 
                                                  font=('Consolas', 10))
        
        # Image input
        self.image_frame = ttk.Frame(self.input_frame)
        self.image_label = ttk.Label(self.image_frame)
        self.image_path_label = ttk.Label(self.image_frame, text="No image selected", 
                                        foreground="gray")
        
        # Audio input
        self.audio_frame = ttk.Frame(self.input_frame)
        self.audio_info = ttk.Label(self.audio_frame, text="No audio file selected", 
                                  foreground="gray")
        
        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Load File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Encode", command=self.encode, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Decode", command=self.decode, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save Output", command=self.save_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT, padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, wrap=tk.WORD,
                                                   font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, ipady=2)
        
        # Configure button styles
        self.style.configure('Accent.TButton', background=self.colors['primary'], 
                           foreground='white')
        self.style.map('Accent.TButton',
                      background=[('active', '#3a6a9c'), ('pressed', '#2a5a8c')])
        
        self.update_ui()
    
    def update_ui(self):
        # Tüm giriş türlerini gizle
        self.text_input.pack_forget()
        self.image_frame.pack_forget()
        self.audio_frame.pack_forget()
        
        # Seçili giriş türünü göster
        self.current_data_type = self.data_type.get()
        if self.current_data_type == "text":
            self.text_input.pack(fill=tk.BOTH, expand=True)
        elif self.current_data_type == "image":
            self.image_frame.pack(fill=tk.BOTH, expand=True)
            self.image_path_label.pack(pady=10)
        elif self.current_data_type == "audio":
            self.audio_frame.pack(fill=tk.BOTH, expand=True)
            self.audio_info.pack(pady=10)
    
    def load_file(self):
        # Seçili veri türüne göre dosya filtreleri belirle
        file_types = []
        if self.current_data_type == "text":
            file_types = [("Text files", "*.txt"), ("All files", "*.*")]
        elif self.current_data_type == "image":
            file_types = [("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        elif self.current_data_type == "audio":
            file_types = [("Audio files", "*.wav"), ("All files", "*.*")]
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return
            
        self.current_file = file_path
        self.show_status(f"Loaded: {os.path.basename(file_path)}")
        
        if self.current_data_type == "text":
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, f.read())
        elif self.current_data_type == "image":
            try:
                image = Image.open(file_path)
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                self.image_path_label.config(text=os.path.basename(file_path))
                self.image_label.pack()
            except Exception as e:
                self.show_status(f"Error loading image: {str(e)}", is_error=True)
        elif self.current_data_type == "audio":
            self.audio_info.config(text=f"Audio file: {os.path.basename(file_path)}")
    
    def encode(self):
        try:
            if self.current_data_type == "text":
                self.encode_text()
            elif self.current_data_type == "image":
                self.encode_image()
            elif self.current_data_type == "audio":
                self.encode_audio()
        except Exception as e:
            self.show_status(f"Error: {str(e)}", is_error=True)
    
    def decode(self):
        try:
            if self.current_data_type == "text":
                self.decode_text()
            elif self.current_data_type == "image":
                self.decode_image()
            elif self.current_data_type == "audio":
                self.decode_audio()
        except Exception as e:
            self.show_status(f"Error: {str(e)}", is_error=True)
    
    def encode_text(self):
        # Metin giriş alanından veriyi al
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            raise ValueError("Input text is empty")
        
        # RLE sıkıştırma algoritmasını uygula
        encoded = []
        count = 1
        
        for i in range(1, len(text)):
            if text[i] == text[i-1]:
                count += 1
            else:
                encoded.append(f"{count}{text[i-1]}")
                count = 1
        
        if text:
            encoded.append(f"{count}{text[-1]}")
            
        result = "".join(encoded)
        original_size = len(text)
        compressed_size = len(result)
        ratio = (1 - (compressed_size / original_size)) * 100
        
        self.display_output(
            f"Encoded: {result}\n\n"
            f"Original size: {original_size} characters\n"
            f"Compressed size: {compressed_size} characters\n"
            f"Compression ratio: {ratio:.2f}%"
        )
        self.show_status("Text encoded successfully!")
    
    def decode_text(self):
        # Metin giriş alanından RLE formatındaki veriyi al
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            raise ValueError("Input text is empty")
            
        # Regex ile sayı-karakter çiftlerini bul
        pairs = re.findall(r'(\d+)([^\d]|\s)', text + ' ')
        if not pairs:
            raise ValueError("Invalid RLE format")
            
        decoded = []
        for count, char in pairs:
            decoded.append(char * int(count))
            
        result = "".join(decoded)
        self.display_output(f"Decoded: {result}")
        self.show_status("Text decoded successfully!")
    
    def encode_image(self):
        # Görüntü dosyasının yüklü olup olmadığını kontrol et
        if not hasattr(self, 'current_file') or not self.current_file:
            raise ValueError("No image file loaded")
            
        try:
            # Görüntüyü aç ve boyutlarını al
            image = Image.open(self.current_file)
            width, height = image.size
            pixels = list(image.getdata())
            
            # RLE için gri tonlamaya çevir
            if image.mode != 'L':
                image = image.convert('L')
                pixels = list(image.getdata())
            
            # Simple RLE on image data
            encoded = []
            count = 1
            current_pixel = pixels[0]
            
            for pixel in pixels[1:]:
                if pixel == current_pixel and count < 255:
                    count += 1
                else:
                    encoded.extend([count, current_pixel])
                    current_pixel = pixel
                    count = 1
            encoded.extend([count, current_pixel])
            
            # Calculate compression ratio
            original_size = len(pixels)
            compressed_size = len(encoded)
            ratio = (1 - (compressed_size / original_size)) * 100
            
            self.display_output(
                f"Image encoded successfully!\n"
                f"Dimensions: {width}x{height}\n"
                f"Original size: {original_size} pixels\n"
                f"Compressed size: {compressed_size} bytes\n"
                f"Compression ratio: {ratio:.2f}%"
            )
            self.encoded_image = encoded
            self.image_size = (width, height)
            self.show_status("Image encoded successfully!")
            
        except Exception as e:
            raise Exception(f"Image encoding failed: {str(e)}")
    
    def decode_image(self):
        # Görüntü dosyasının yüklü olup olmadığını kontrol et
        if not hasattr(self, 'encoded_image') or not hasattr(self, 'image_size'):
            raise ValueError("No encoded image data available")
            
        try:
            # Decode RLE data
            decoded = []
            for i in range(0, len(self.encoded_image), 2):
                if i + 1 >= len(self.encoded_image):
                    break
                count = self.encoded_image[i]
                value = self.encoded_image[i+1]
                decoded.extend([value] * count)
            
            # Create image from decoded data
            width, height = self.image_size
            image = Image.new('L', (width, height))
            image.putdata(decoded)
            
            # Save the decoded image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            
            if save_path:
                image.save(save_path)
                self.show_status(f"Image decoded and saved to {save_path}")
                self.display_output(f"Image saved to:\n{save_path}")
                
        except Exception as e:
            raise Exception(f"Image decoding failed: {str(e)}")
    
    def encode_audio(self):
        # Ses dosyasının yüklü olup olmadığını kontrol et
        if not hasattr(self, 'current_file') or not self.current_file:
            raise ValueError("No audio file loaded")
            
        try:
            # WAV dosyasını oku ve parametrelerini al
            with wave.open(self.current_file, 'rb') as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(params.nframes)
                
            # İşlem için numpy dizisine çevir
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Simple RLE on audio data
            encoded = []
            count = 1
            for i in range(1, len(audio_data)):
                if audio_data[i] == audio_data[i-1]:
                    count += 1
                    if count == 255:  # Limit run length
                        encoded.extend([count, audio_data[i-1]])
                        count = 1
                else:
                    encoded.extend([count, audio_data[i-1]])
                    count = 1
            
            if len(audio_data) > 0:
                encoded.extend([count, audio_data[-1]])
                
            # Calculate compression ratio
            original_size = len(audio_data) * 2  # 2 bytes per sample
            compressed_size = len(encoded) * 2   # 2 bytes per value
            ratio = (1 - (compressed_size / original_size)) * 100
            
            self.display_output(
                f"Audio encoded successfully!\n"
                f"Original size: {original_size} bytes\n"
                f"Compressed size: {compressed_size} bytes\n"
                f"Compression ratio: {ratio:.2f}%"
            )
            self.encoded_audio = encoded
            self.audio_params = params
            self.show_status("Audio encoded successfully!")
            
        except Exception as e:
            raise Exception(f"Audio encoding failed: {str(e)}")
    
    def decode_audio(self):
        # Ses dosyasının yüklü olup olmadığını kontrol et
        if not hasattr(self, 'encoded_audio') or not hasattr(self, 'audio_params'):
            raise ValueError("No encoded audio data available")
            
        try:
            # Decode RLE data
            decoded = []
            for i in range(0, len(self.encoded_audio), 2):
                if i + 1 >= len(self.encoded_audio):
                    break
                count = self.encoded_audio[i]
                value = self.encoded_audio[i+1]
                decoded.extend([value] * count)
            
            # Convert back to 16-bit audio data
            audio_data = np.array(decoded, dtype=np.int16)
            
            # Save the decoded audio
            save_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")])
            
            if save_path:
                with wave.open(save_path, 'wb') as wav_file:
                    wav_file.setparams(self.audio_params)
                    wav_file.writeframes(audio_data.tobytes())
                
                self.show_status(f"Audio decoded and saved to {save_path}")
                self.display_output(f"Audio saved to:\n{save_path}")
                
        except Exception as e:
            raise Exception(f"Audio decoding failed: {str(e)}")
    
    def save_output(self):
        # Çıktı metnini al
        output = self.output_text.get("1.0", tk.END).strip()
        if not output:
            messagebox.showwarning("Warning", "No output to save")
            return
            
        # Kaydetme iletişim kutusu aç
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(output)
            self.show_status(f"Output saved to {file_path}")
    
    def clear_all(self):
        # Metin alanlarını temizle
        self.text_input.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        # Mevcut dosya bilgisini sıfırla
        self.current_file = None
        self.show_status("Cleared all fields")
    
    def display_output(self, text):
        # Çıktı alanını temizle ve yeni metni ekle
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
    
    def show_status(self, message, is_error=False):
        # Durum çubuğunda mesaj göster
        self.status_var.set(message)
        # Hata mesajı ise 5 saniye sonra "Ready" yap
        if is_error:
            self.root.after(5000, lambda: self.status_var.set("Ready"))

if __name__ == "__main__":
    root = tk.Tk()
    app = RLECompressorApp(root)
    root.mainloop()