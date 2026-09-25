#!/usr/bin/env python3

import argparse
import ROOT
from base.helpers import get_bin_content_by_name


def rescale_histograms(root_file, systematic):
    # Find all cutFlowHisto_*_<systematic>Up/Down histograms.
    cutflow_histograms = []

    for key in root_file.GetListOfKeys():
        name = key.GetName()

        if (
            name.startswith("cutFlowHisto_")
            and name.endswith(f"_{systematic}Down")
        ) or (
            name.startswith("cutFlowHisto_")
            and name.endswith(f"_{systematic}Up")
        ):
            cutflow_histograms.append(name)

    for variation_cutflow_name in cutflow_histograms:

        if variation_cutflow_name.endswith(f"_{systematic}Down"):
            variation = "Down"
        else:
            variation = "Up"

        # Extract the part between "cutFlowHisto_" and "_<systematic><variation>"
        prefix = variation_cutflow_name[
            len("cutFlowHisto_"):
            -len(f"_{systematic}{variation}")
        ]

        nominal_cutflow_name = f"cutFlowHisto_{prefix}_nominal"

        variation_cutflow = root_file.Get(variation_cutflow_name)
        nominal_cutflow = root_file.Get(nominal_cutflow_name)

        if not variation_cutflow:
            print(f"WARNING: Missing {variation_cutflow_name}")
            continue

        if not nominal_cutflow:
            print(f"WARNING: Missing {nominal_cutflow_name}")
            continue

        variation_norm = get_bin_content_by_name(variation_cutflow, "Skim")
        nominal_norm   = get_bin_content_by_name(nominal_cutflow, "Skim")

        if variation_norm == 0:
            print(
                f"WARNING: {variation_cutflow_name} has zero "
                "content in bin 2; skipping."
            )
            continue

        scale_factor = nominal_norm / variation_norm

        print(
            f"{variation_cutflow_name}: "
            f"{variation_norm:.6g} -> {nominal_norm:.6g}, "
            f"scale = {scale_factor:.6g}"
        )

        prefix_pieces = prefix.split("_")
        # Histograms to be rescaled.
        patterns = []
        for cat in ["pass", "fail"]:
            histo_prefix = "_".join([prefix_pieces[0], cat, prefix_pieces[-1]])
            patterns.extend([
                f"j3_{histo_prefix}_{systematic}{variation}",
                f"mjj_vs_mjjj_{histo_prefix}_{systematic}{variation}",
            ])

        for histogram_name in patterns:
            histogram = root_file.Get(histogram_name)

            if not histogram:
                print(f"  WARNING: Missing {histogram_name}")
                continue

            histogram.Scale(scale_factor)

            # Write the modified histogram back with the same name.
            histogram.Write(histogram_name, ROOT.TObject.kOverwrite)

            print(f"  Rescaled {histogram_name}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Rescale systematic variation histograms so that their "
            "normalization matches the nominal sample normalization."
        )
    )

    parser.add_argument("-i", "--input", dest="input",
                        help="Input ROOT file",
                        required=True,
                        metavar="INPUT")
    parser.add_argument("-s", "--syst", dest="systematic",
                        help="Systematic variations  (default: %(default)s)",
                        nargs="*",
                        choices=["FSRPartonShower", "ISRPartonShower", "PDF_weight", "PDFaS_weight", "aS_weight", "scalevar_7pt"],
                        default=["FSRPartonShower", "ISRPartonShower", "PDF_weight", "PDFaS_weight", "aS_weight", "scalevar_7pt"],
                        metavar="SYST")

    args = parser.parse_args()

    root_file = ROOT.TFile.Open(args.input, "UPDATE")

    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"Could not open ROOT file: {args.input}")

    for syst in args.systematic:
        rescale_histograms(root_file, syst)
    
    root_file.Close()


if __name__ == "__main__":
    main()
