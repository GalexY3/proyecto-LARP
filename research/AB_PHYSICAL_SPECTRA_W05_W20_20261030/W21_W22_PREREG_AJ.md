# W21 and W22 — two final AB-R preregistered source-validation and colorimetry contrasts
Date: 2026-10-30. This completes the 20-item new authorized block IF validly executed. W03/W04 (2) + W05-W20 (16) = 18, NOT 20. Previous inaccurate subtotal was corrected explicitly to the user. Prior old grant unspent 9 remains separate. W21/W22 cannot be replaced by more GP/Fourier or toy N400 patterns.

## W21 — raw-to-averaged laboratory reproducibility of new physical source
A Estimand: per-measurement numerical agreement between raw-replicate mean and archived averaged spectral series, for 401 wavelengths 350..750, PLUS within-series replicate discrepancies; unit = 5 repeated instrument/material pair sets, not each 1nm wavelength as independent replicate.
B H0 mean of two named repeats equals averaged series to rounding; H1 differences due to other averaging/preprocessing; H2 source anomaly, malformed CSV.
C Tests: 550nm filter raw '550 nm','550 nm (2)' vs averaged '550 nm'; large/small checkerboard black/white raw (1,2) vs single averaged; 32 direct original names (6 filters not 550; printer white/toner; all 24 ColorChecker) vs archived averaged. Predeclare max absolute tolerance 0.00001 to accommodate CSV rounding. Repeated pair RMS discrepancies reported, no inference to all instruments.
D Freeze W21 code in GitHub before requesting rows 350–750 of `spectra_named.csv`; headers have already been read, not values. Source `bllanos/chromatic-aberration@9350e51a1ca96d541a6a82627fd0bf7636cf6638`, blob named ab00192d9b537d4b7942357ee7f2ed30ee623b12, averaged 82b83444716930c75e1d2a77ac6eed9fd6ccdc8d. Full raw has quoted header with comma, CSV parser MUST handle quotes.
E Fetch 402 lines (including header) of both files and run frozen script once, rerun exact output, archive all five and direct control values. No raw data redistribution.
F Failure/errata retained. Source may average in ways not captured by simple pair arithmetic; either way not independent instrument replication; no MHU inference.
G Repeat of source identical = software replay only; no outside measurement.
H Prior of spectrometry provenance conditional on repeat arithmetic.
I Novelty grade 0/3; CT2 N400 math 24 and functional 18 unchanged.
J STOP rereading same CSV after this audit; next scientific observation must be spatial 5+ bands + valid Wei controls.

## W22 — independent CIE1931 reference-weighted impact of band subsampling
A Estimand: equal-energy-illuminant CIE XYZ integrated squared error of heldout ColorChecker reflectance patches under two five-band reconstruction strategies (fixed 400,470,550,620,700 vs W13 development-greedy 400,470,530,610,700). Population observed: 12 held-out patches, not independent human observers. XYZ uses 31 points at 400–700nm/10nm, common scaling by sum ybar on same grid; note no measured source illuminant or detector spectral response, so **hypothetical equal-energy tristimulus**, not measured color perception.
B H0 greedy has smaller XYZ error even if unweighted spectrum MSE was worse; H1 fixed dominates XYZ too; H2 differences negligible. No claimed scientifically significant effect.
C Controls: same CIE table, same 12 heldout measured reflectances, same five channels and linear interpolation, no posterior tuning. Primary outcome ratio greedy/fixed squared XYZ error, plus per-patch paired sign count and unweighted comparison archived from W13. No 3-band RGB reconstruction shortcut.
D Code frozen in GitHub before reading full CIE table (headerless numeric schema 1st two lines seen). Source CIE official DOI 10.25039/CIE.DS.xvudnb9b; machine-readable independent public copy `sblisesivdin/spectrum-to-rgb` CIE_xyz_1931_2deg.csv blob 9b4e3f73b4bb412a762a6d03cb8060bfea652a6e. Pin repo commit after verifying Git ref, no license agreements accepted or original tables republished.
E Execute the exact frozen code; archive per-patch derived errors and group mean only.
F Calibration spectra are reflectances relative to standards, not a calibrated illuminant spectral radiance. CIE1931 X/Y/Z does not establish that colors are perceptually equivalent nor apply to vision model from LARP. A weighted metric selected post W13 is explorative and selection-exposed, not confirmation.
G Separate fresh external data not obtained; CIE is an independent standardized response function, not independent sample of new laboratory scenes.
H Prior: spectral MSE ranking can be estimand-dependent (test direction).
I grade 0/3, CT2 unchanged.
J No 2/3 claim; R5 STOP this lab source after W22.
