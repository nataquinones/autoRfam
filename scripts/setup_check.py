import os
import sys


def check_config_paths(paths):
    """
    Goes and checks the existance of the programs specified in config file, as
    specified by -e option and imported through import_config() function.
    """

    # Check if nhmmer exists and is right
    if not (os.path.exists(paths.nhmmerpath) &
            (os.path.basename(paths.nhmmerpath) == "nhmmer")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: nhmmer"
        print "#"
        print "# I'm looking for: '%s' " % paths.nhmmerpath
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.nhmmerpath) != "nhmmer":
            print "# The basename is '%s',"\
                  " but I expect it to be 'nhmmer'."\
                  % os.path.basename(paths.nhmmerpath)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    # Check if nhmmer exists and is right
    if not (os.path.exists(paths.eslalistat) &
            (os.path.basename(paths.eslalistat) == "esl-alistat")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: esl-alistat"
        print "#"
        print "# I'm looking for: '%s' " % paths.eslalistat
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.eslalistat) != "esl-alistat":
            print "# The basename is '%s',"\
                  " but I expect it to be 'esl-alistat'."\
                  % os.path.basename(paths.eslalistat)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    # Check if esl-reformat exists and is right
    if not (os.path.exists(paths.eslref) &
            (os.path.basename(paths.eslref) == "esl-reformat")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: esl-reformat"
        print "#"
        print "# I'm looking for: '%s' " % paths.eslref
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.eslalistat) != "esl-reformat":
            print "# The basename is '%s',"\
                  " but I expect it to be 'esl-reformat'."\
                  % os.path.basename(paths.eslref)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    # Check if R-scape exists and is right
    if not (os.path.exists(paths.rscapepath) &
            (os.path.basename(paths.rscapepath) == "R-scape")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: R-scape"
        print "#"
        print "# I'm looking for: '%s' " % paths.rscapepath
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.rscapepath) != "R-scape":
            print "# The basename is '%s',"\
                  " but I expect it to be 'R-scape'."\
                  % os.path.basename(paths.rscapepath)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    # Check if R-scape exists and is right
    if not (os.path.exists(paths.rscapepath) &
            (os.path.basename(paths.rscapepath) == "R-scape")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: R-scape"
        print "#"
        print "# I'm looking for: '%s' " % paths.rscapepath
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.rscapepath) != "R-scape":
            print "# The basename is '%s',"\
                  " but I expect it to be 'R-scape'."\
                  % os.path.basename(paths.rscapepath)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    # Check if RNAcode exists and is right
    if not (os.path.exists(paths.rnacodepath) &
            (os.path.basename(paths.rnacodepath) == "RNAcode")):
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# autoRfam"
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        print "# Can't find: RNAcode"
        print "#"
        print "# I'm looking for: '%s' " % paths.rnacodepath
        print "# as indicated in: '%s'" % paths.__file__
        if os.path.basename(paths.rnacodepath) != "RNAcode":
            print "# The basename is '%s',"\
                  " but I expect it to be 'RNAcode'."\
                  % os.path.basename(paths.rnacodepath)
        else:
            print "# Try selecting the correct -e option"\
                   "or ammending this config file."
        print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        sys.exit(1)

    return paths


def check_outdir(args):
    """
    Depending on what's indicated in -o option:
    Defines the default out_dir or
    checks if the specified out_dir is valid.
    """
    if args.outdir == "default_dir":
        name = os.path.splitext(os.path.basename(os.path.abspath(args.input_urs)))[0]
        out_dir = os.path.join(os.path.dirname(os.path.abspath(args.input_urs)), "autoRfam_%s" % name)
    else:
        if os.path.exists(os.path.abspath(args.outdir)):
            if os.path.isfile(os.path.abspath(args.outdir)):
                print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                print "# autoRfam"
                print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                print "# Invalid -o: Please select a valid path."
                print "# Problem:"
                print "# '%s'" % os.path.abspath(args.outdir)
                print "# is not a directory."
                print "#"
                print "# For help: autoRfam.py -h"
                print "- - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                sys.exit(1)

            else:
                out_dir = os.path.abspath(args.outdir)

        else:
            absdir_path = os.path.abspath(os.path.dirname(args.outdir))
            if os.path.exists(absdir_path):
                out_dir = os.path.abspath(args.outdir)
            else:
                print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                print "# autoRfam"
                print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                print "# Invalid -o: Please select a valid path."
                print "# Problem:"
                print "# Can't create '%s', because" % args.outdir
                print "# '%s' doesn't exist." % absdir_path
                print "#"
                print "# For help: autoRfam.py -h"
                print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                sys.exit(1)

    return out_dir
