class FXLMS:
	def __init__(self, alpha):
		self.alpha = alpha
		return

	def calcNewCoef(self, a_n, signal, error_n, alpha):
		self.alpha = alpha
		return a_n + 2 * self.alpha * signal * error_n


import librosa
import numpy as np

def spectral_subtraction(noisy_audio, fs, n_fft=2048, hop_length=512):
    # Compute the Short-Time Fourier Transform (STFT)
    D_noisy = librosa.stft(noisy_audio, n_fft=n_fft, hop_length=hop_length)
    magnitude_noisy, phase_noisy = librosa.magphase(D_noisy)
    
    # Estimate the noise magnitude (this is an assumption based on silence or low energy parts)
    noise_estimate = np.median(magnitude_noisy, axis=1, keepdims=True)
    
    # Subtract the noise estimate from the noisy signal
    magnitude_clean = magnitude_noisy - noise_estimate
    magnitude_clean[magnitude_clean < 0] = 0  # Ensure no negative magnitudes
    
    # Reconstruct the clean signal
    D_clean = magnitude_clean * phase_noisy
    cleaned_audio = librosa.istft(D_clean, hop_length=hop_length)
    
    return cleaned_audio