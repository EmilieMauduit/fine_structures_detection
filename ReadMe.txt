This is the repository containing the code used in : 
Mauduit, E., Zarka, P. et al. Drifting discrete Jovian radio bursts reveal acceleration processes related to Ganymede and the main aurora., Nat Commun 14, 5981 (2023). https://doi.org/10.1038/s41467-023-41617-8



--------------------
Figures : directory containing the python code used to produce the figures of the article, along with the saveset containing the data.
--------------------

figures_article.py --> Contains, in the right order and labeled, the codes used to produce the figures present in the article.

jupiter_sf.py --> Contains useful functions used in 'figures_article.py'.

data.sav --> Saveset containing all the data obtained by the processing pipeline, for both left-handed and right-handed polarisation.

--------------------
Processing : directory containing all IDL routines used to process and analyse the data.
--------------------

junolib.pro --> library containing useful function for JUNO data

band_decomp.pro --> decompose a frequency range in bands of the same size with an overlap of ~1MHz

deparasitage.pro --> perform RFI mitigation on a given chunk of data

mask_tf.pro --> function used to clean the 2D-FFT of a given chunk of data (after having applied 'deparasitage.pro')

prep_ponderation.pro --> compute the Radon transform of a box full of ones, with the same size as the chunk of data being processed.

traitement_junon.pro --> perform the full processing of a given chunk of data (RFI mitigation, 2D-FFT, Radon transform)

peakcentering.pro --> find the peak in a 1D spectra and places the maximum at the center

peakmodel.pro --> fit with a gaussian a peak in a 1D spectra

plot_data.pro --> plots in one line the clean chunk of data, its 2D-FFT and its Radon transform

snr_func.pro --> compute the SNR value of peak using the parameters from peakmodel.pro

true_angle.pro --> retrieve the 'true' angle of a given index in the 1D spectra (values are moved around in peakcentering)

junon_sampling_v2.pro --> main routine : open every observation and perform the processing and analysis of the data, produce the final outputs and plots along the way
