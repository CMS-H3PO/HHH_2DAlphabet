FIT_DEFAULTS_SINGLE = {
    "defMinStrat": 2,
    "rMin": -5,
    "rMax": 5,
    "extra": "",
}

FIT_DEFAULTS_COMBINED = {
    "defMinStrat": 2,
    "rMin": -5,
    "rMax": 5,
    "extra": "--cminDefaultMinimizerTolerance 0.01",
}

# Keys in the following format
# ("YEAR", "CHANNEL", "REGION", "POLYORDER")
FIT_OVERRIDES = {
    ("Run2", "*", "*", "*"): {
        "extra": "--cminDefaultMinimizerTolerance 0.01",
    },

    ("*", "*", "SR_pass_toy", "*"): {
        "rMin": -1,
        "rMax": 1
    },

    ("*", "*", "SR_pass_toy_fullSyst", "*"): {
        "rMin": -1,
        "rMax": 1
    },

    ("*", "*", "SR_pass_toy_multiSignal", "*"): {
        "rMin": -1,
        "rMax": 1
    },

    ("*", "*", "SR_pass_toy_multiSignal_fullSyst", "*"): {
        "rMin": -1,
        "rMax": 1
    },

    ("2017", "boosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "5.80",
            "qcd_rpfT_1_par1": "-1.00",
            "qcd_rpfT_1_par2": "-0.50",
        },
    },

    ("2017", "semiboosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "5.60",
            "qcd_rpfT_1_par1": "-4.10",
            "qcd_rpfT_1_par2":  "0.10",
        },
    },

    ("2017", "semiboosted", "VR", "3"): {
        "defMinStrat": 1,
    },

    ("Run2", "boosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "6.70",
            "qcd_rpfT_1_par1": "-2.00",
            "qcd_rpfT_1_par2": "-0.20",
        },
        "extra": "",
    },

    ("Run2", "boosted", "VR", "2"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "boosted", "VR", "3"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "boosted", "VR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "6.20",
            "qcd_rpfT_1_par1": "-2.00",
            "qcd_rpfT_1_par2": "-0.10",
        },
    },

    ("Run2", "boosted", "SR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "6.20",
            "qcd_rpfT_1_par1": "-1.30",
            "qcd_rpfT_1_par2": "-1.50",
        },
    },

    ("Run2", "boosted", "SR_pass_toy", "2"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "boosted", "SR_pass_toy", "3"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "semiboosted", "VR", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "3.80",
            "qcd_rpfT_1_par1": "-2.20",
            "qcd_rpfT_1_par2":  "0.20",
        },
        "extra": "",
    },

    ("Run2", "semiboosted", "VR", "2"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "semiboosted", "VR", "3"): {
        "defMinStrat": 1,
        "extra": "",
    },

    ("Run2", "semiboosted", "VR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "4.70",
            "qcd_rpfT_1_par1": "-2.90",
            "qcd_rpfT_1_par2":  "0.17",
        },
    },

    ("Run2", "semiboosted", "SR_pass_toy", "1"): {
        "setParams": {
            "qcd_rpfT_1_par0":  "3.80",
            "qcd_rpfT_1_par1": "-2.20",
            "qcd_rpfT_1_par2":  "0.20",
        },
    },

    ("Run2", "semiboosted", "SR_pass_toy", "2"): {
        "defMinStrat": 0,
        "extra": "",
    },

    ("Run2", "semiboosted", "SR_pass_toy", "3"): {
        "defMinStrat": 0,
        "extra": "",
    },

    ("2017", "combined", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":  "-1.00",
            "qcd_b_rpfT_1_par2":  "-0.50",
            "qcd_sb_rpfT_1_par0":  "5.60",
            "qcd_sb_rpfT_1_par1": "-4.20",
            "qcd_sb_rpfT_1_par2":  "0.15"
        },
    },

    ("Run2", "combined", "VR", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "6.70",
            "qcd_b_rpfT_1_par1":  "-2.00",
            "qcd_b_rpfT_1_par2":  "-0.20",
            "qcd_sb_rpfT_1_par0":  "3.80",
            "qcd_sb_rpfT_1_par1": "-2.20",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },

    ("Run2", "combined", "VR_pass_toy", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "7.08",
            "qcd_b_rpfT_1_par1":  "-2.76",
            "qcd_b_rpfT_1_par2":  "-0.06",
            "qcd_sb_rpfT_1_par0":  "5.30",
            "qcd_sb_rpfT_1_par1": "-3.50",
            "qcd_sb_rpfT_1_par2":  "0.20"
        },
    },

    ("Run2", "combined", "SR_pass_toy", "1:1"): {
        "defMinStrat": 0,
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":   "0.10",
            "qcd_b_rpfT_1_par2":  "-2.50",
            "qcd_sb_rpfT_1_par0":  "5.20",
            "qcd_sb_rpfT_1_par1": "-4.40",
            "qcd_sb_rpfT_1_par2":  "1.00"
        },
        "extra": "--cminDefaultMinimizerTolerance 0.1",
    },

    ("Run2", "combined", "SR_pass_toy_fullSyst", "1:1"): {
        "defMinStrat": 0,
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":   "0.10",
            "qcd_b_rpfT_1_par2":  "-2.50",
            "qcd_sb_rpfT_1_par0":  "5.20",
            "qcd_sb_rpfT_1_par1": "-4.40",
            "qcd_sb_rpfT_1_par2":  "1.00"
        },
        "extra": "--cminDefaultMinimizerTolerance 0.1",
    },

    ("Run2", "combined", "SR_pass_toy_multiSignal", "1:1"): {
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":   "0.10",
            "qcd_b_rpfT_1_par2":  "-2.50",
            "qcd_sb_rpfT_1_par0":  "5.20",
            "qcd_sb_rpfT_1_par1": "-4.40",
            "qcd_sb_rpfT_1_par2":  "1.00"
        },
    },

    ("Run2", "combined", "SR_pass_toy_multiSignal_fullSyst", "1:1"): {
        "defMinStrat": 0,
        "setParams": {
            "qcd_b_rpfT_1_par0":   "5.80",
            "qcd_b_rpfT_1_par1":   "0.10",
            "qcd_b_rpfT_1_par2":  "-2.50",
            "qcd_sb_rpfT_1_par0":  "5.20",
            "qcd_sb_rpfT_1_par1": "-4.40",
            "qcd_sb_rpfT_1_par2":  "1.00"
        },
        "extra": "--cminDefaultMinimizerTolerance 0.1",
    },
}

BESTORDER_DEFAULT_BOOSTED     = "1"
BESTORDER_DEFAULT_SEMIBOOSTED = "1"
BESTORDER_DEFAULT_COMBINED    = "1:1"

BESTORDER_OVERRIDES = {
    "2017_boosted_VR": "0",
}

SIGNAL_OVERRIDES = {
}
