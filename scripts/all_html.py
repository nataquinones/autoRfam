"""
"""
import re
import requests
import pandas as pd
import os
import shutil
import sys
import glob

# ..............PARAMS...............
TIME_OUT = 60
PUBLICATIONS_PAGESIZE = 10
pd.set_option('max_colwidth', -1)
RSCAPE_FOLDER = "rscape"
RNACODE_FOLDER = "rnacode"

# .............................FUNCTIONS...................................


def easelstats_table(eslalistat, stoali):
    """
    Calculates alignments statistics with esl-alistat for all the
    alignments in a given path. Makes pandas dataframe with results.
    --
    eslalistat = path to esl-alistat software
    stoali = folder with alignemnts
    """
    cmd = eslalistat + " --rna %s" % (stoali)
    result = os.popen(cmd).readlines()
    values = []

    for line in result:
        values.append(line.split()[-1])

    num_seq = int(values[2])
    alen = int(values[3])
    diff = int(values[6]) - float(values[5])
    avlen = float(values[7])
    lenalen_ratio = avlen / alen
    avid = int(values[8].strip("%"))
    df_easelstats = pd.DataFrame([num_seq,
                                  alen,
                                  diff,
                                  avlen,
                                  round(lenalen_ratio, 2),
                                  avid], dtype=object)
    df_easelstats["in"] = ["Number of sequences",
                           "Alignment length",
                           "Max-Min lengths",
                           "Avg. length",
                           "Length-Alignment length ratio",
                           "Avg. per. id"]
    df_easelstats = df_easelstats.set_index("in")
    del df_easelstats.index.name

    return df_easelstats


def extract_ursdesc(stoali):
    """
    Takes stockholm file and extracts sequence name
    and description into tuple
    """
    readfile = open(stoali, "r")
    read = readfile.read()
    readfile.close()
    urs = re.findall(r"(?<=#=GS\s)(URS.{10})", read)
    desc = re.findall(r"(?<=DE\s)(.*)", read)
    df_desc = pd.DataFrame()
    df_desc["urs"] = urs
    df_desc["description"] = desc
    df_desc.index += 1
    df_desc["seq"] = df_desc.index
    df_desc = df_desc[["seq", "urs", "description"]]

    return df_desc


def publications_table(urs):
    """
    Takes list of urs, fetches publication info from RNAcentral
    """
    df_publications = pd.DataFrame()
    # fetch publication info for each urs
    for i in urs:
        urlpubs = "http://rnacentral.org/api/v1/rna/"\
                  "%s/"\
                  "publications?page_size=%i" % (i, PUBLICATIONS_PAGESIZE)
        try:
            req = requests.get(urlpubs, timeout=TIME_OUT)
            data = req.json()
            # fetch the relevant parameters publication
            num_ref = len(data["results"])
            for j in range(0, num_ref):
                # values for table
                pubmed = str(data['results'][j]["pubmed_id"])
                title = str(data['results'][j]["title"])
                # write into line
                line = [[i,
                         pubmed,
                         title]]
                # only append if it has a pubmed id
                if str(data['results'][j]["pubmed_id"]) != "None":
                    df_publications = df_publications.append(line)
        # if timeout, add line indicating it
        except requests.exceptions.Timeout:
            line = [[i, "timeout", "timeout"]]
            df_publications = df_publications.append(line)
    # .. add tables titles
    if len(df_publications) != 0:
        df_publications.columns = ["urs", "pubmed_id", "title"]
        df_publications = df_publications.drop_duplicates("pubmed_id")
        df_publications = df_publications[["pubmed_id", "title"]]
    return df_publications


def request_xrefs(urs):
    """
    Takes list of urs, fetches urs info from RNAcentral
    """
    df_xrefs = pd.DataFrame()
    # fetch xrefs info for each urs
    for i in urs:
        urlxrefs = "http://rnacentral.org/api/v1/rna/%s/xrefs" % i

        try:
            req = requests.get(urlxrefs, timeout=TIME_OUT)
            data = req.json()
            # fetch the relevant parameters per xref
            num_db = len(data["results"])
            if num_db != 0:
                for j in range(0, num_db):
                    # values for table
                    urs_link = "<a href=\"http://rnacentral.org/rna/%s\" target=\"_blank\">%s</a>" % (i, i)
                    db_name = str(data["results"][j]["database"])

                    if data["results"][j]["is_expert_db"] == True:
                        source_url = str(data["results"][j]["accession"]["expert_db_url"])

                    else:
                        source_url = str(data["results"][j]["accession"]["source_url"])
                    db_link = "<a href=\"%s\" target=\"_blank\">%s</a>" % (source_url, db_name)
                    rna_type = str(data["results"][j]["accession"]["rna_type"])
                    product = str(data["results"][j]["accession"]["product"])
                    taxid = str(data["results"][j]["taxid"])
                    species = str(data["results"][j]["accession"]["species"])
                    # write into line
                    line = [[i,
                             urs_link,
                             db_name,
                             db_link,
                             rna_type,
                             product,
                             taxid,
                             species]]
            else:
                line = [[i,
                         "error_no_db",
                         "error_no_db",
                         "error_no_db",
                         "error_no_db",
                         "error_no_db",
                         "error_no_db",
                         "error_no_db"]]

            # append line into df
            df_xrefs = df_xrefs.append(line)

        # if timeout, add line indicating it
        except requests.exceptions.Timeout:
            line = [[i,
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout"]]
            df_xrefs = df_xrefs.append(line)
    # add column names
    df_xrefs.columns = ["urs",
                        "urs_link",
                        "db",
                        "db_link",
                        "rna_type",
                        "product",
                        "tax_id",
                        "species"]
    # clean and return
    df_xrefs = df_xrefs.reset_index(drop=True)

    return df_xrefs


def dominant_type(df_xrefs):
    """
    """
    dominant = df_xrefs["rna_type"].value_counts().index[0]

    return dominant


def database_table(df_xrefs):
    """
    """
    database_df = pd.DataFrame(df_xrefs["db"].value_counts())

    return database_df


def rnatype_table(df_xrefs):
    """
    """
    rnatype_df = pd.DataFrame(df_xrefs["rna_type"].value_counts())

    return rnatype_df


def fullinfo_table(df_desc, df_xrefs):
    """
    """
    fullinfo_df = df_desc.set_index("urs").join(df_xrefs.set_index("urs"))
    fullinfo_df = fullinfo_df[["seq",
                               "urs_link",
                               "description",
                               "db_link",
                               "rna_type",
                               "product",
                               "tax_id",
                               "species"]]
    fullinfo_df = fullinfo_df.set_index(["seq"])
    fullinfo_df = fullinfo_df.sort_index()
    fullinfo_df.reset_index(level=0, inplace=True)

    return fullinfo_df


def check_rnacode(stoali):
    """
    """
    rnacode_results = os.path.join(os.path.dirname(stoali), RNACODE_FOLDER)
    epsfiles = glob.glob(os.path.join(rnacode_results, "*.eps"))

    if len(epsfiles) != 0:
        codingwarn = True

    else:
        codingwarn = False

    return codingwarn


def check_rscape(stoali):
    """
    """
    rscspe_results = os.path.join(os.path.dirname(stoali), RSCAPE_FOLDER)
    outfile = glob.glob(os.path.join(rscspe_results, "*.out"))[0]

    if os.stat(outfile).st_size != 0:
        rscapewarn = True

    else:
        rscapewarn = False

    return rscapewarn


def make_html(eslalistat, stoali):
    """
    """

    aliname = os.path.basename(stoali)
    df_desc = extract_ursdesc(stoali)
    urs = df_desc["urs"]
    df_xrefs = request_xrefs(urs)

    # .. TABLES
    # ..... alignment statistics
    df_easelstats = easelstats_table(eslalistat, stoali)
    easelstats_html = df_easelstats.to_html(header=False,
                                            index=True,
                                            escape=False,
                                            classes='df')
    # ..... publications
    df_publications = publications_table(urs)
    publications_html = df_publications.to_html(header=True,
                                                index=False,
                                                escape=False,
                                                classes='df')
    # ..... database annotations
    database_df = database_table(df_xrefs)
    database_html = database_df.to_html(header=False,
                                        index=True,
                                        escape=False,
                                        classes='df')
    # ..... rnatype annotations
    rnatype_df = rnatype_table(df_xrefs)
    rnatype_html = rnatype_df.to_html(header=False,
                                      index=True,
                                      escape=False,
                                      classes='df')

    # ..... full information
    fullinfo_df = fullinfo_table(df_desc, df_xrefs)
    fullinfo_html = fullinfo_df.to_html(header=True,
                                        index=False,
                                        escape=False,
                                        classes='sortable')


    # .. RSCAPE & RNACODE
    # .....RNAcode
    if check_rnacode(stoali):
        rnacode_html = "<b>WARNING! </b>"\
                      "This alignment has coding potential. "\
                      "<font size='2' color='grey'>"\
                      "<a href=\"%s\">"\
                      "<i>[Explore RNAcode results]</i>"\
                      "</a>"\
                      "</font>\n" % (os.path.join(".", RNACODE_FOLDER))
    else:
        rnacode_html = "No coding potential found. "\
                      "<font size='2' color='grey'>"\
                      "<a href=\"%s\"><i>"\
                      "[Explore RNAcode results]</i>"\
                      "</a>"\
                      "</font>\n" % (os.path.join(".", RNACODE_FOLDER))
    # ....Rscape
    rscape_img = os.path.join(os.path.join(os.path.dirname(stoali), RSCAPE_FOLDER), "*.cyk.R2R.sto.svg")

    if len(glob.glob(rscape_img)) != 0:
        img_src = glob.glob(rscape_img)[0]
        rscape_html = "<img src=%s>" % os.path.join(".", RSCAPE_FOLDER, os.path.basename(img_src))

    else:
        rscape_html = "R-scape image not available"

    # .. OTHER HTML
    browse_ali = "../../HOME.html"
    header = """
             <html>
                   <head>
                         <title>%s</title>
                         <script src="../../sorttable.js"></script>
                   </head>
             """ % aliname
    body = """
           <body style="font-family:'helvetica';
                        margin-top: 1%;
                        margin-bottom: 1%;
                        margin-right: 4%;
                        margin-left: 2%;"
                        link="#3366BB"
                        vlink="#663366">
           """
    style = """
            <style>
                    h1{color: #7a0606;
                       font-family: helvetica;
                       font-weight:normal;
                       font-size: 350%}
                    h2, h3 {color: #822424;
                       font-family: helvetica;
                       font-weight:normal;
                       display: inline;}
                    .df
                    th {text-align: left;
                        background-color: #822424;
                        color: white;
                        font-family:helvetica;}
                    table {border-collapse: collapse;}
                    table, th, td {border: 1px solid black;
                                   font-family: monospace;
                                   font-size:12px;
                                   font-weight:normal;
                                   padding:5px 10px;
                                   border-style:solid;
                                   border-width:1px;}
                    tr:hover {background-color: #e8e5e5}

                    table.sortable th {text-align: left;
                                       background-color: #822424;
                                       color: white;
                                      font-weight: normal;
                                      font-family:helvetica;}
                    table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after { 
                    content: ' \\25B9'}
            </style>
            """
    footer = """
                    </body>
             </html>
             """

    # .. WRITE HTML
    out_html = stoali + ".html"
    with open(out_html, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(style)
        f.write("\n")
        f.write("<div align='right'>\n")
        f.write("<font size='2' color='grey'>")
        f.write("<a href='%s'>browse alignments</a> > alignment %s \n" % (browse_ali, aliname))
        f.write("</font>\n")
        f.write("</div>\n")
        f.write("<h1>autoRfam\n")
        f.write("    <font size='5' color='grey'>\n")
        f.write("        <i>alignment %s</i>\n" % aliname)
        f.write("    </font>\n")
        f.write("</h1>\n")
        f.write("<br>\n")
        f.write("<div style='margin-left:2%'>\n")
        f.write("<h2>Alignment statistics</h2>\n")
        f.write("<hr />\n")
        f.write(easelstats_html + "\n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>Publications</h2>\n")
        f.write("<hr />\n")
        f.write(publications_html + "\n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>Database annotations</h2>\n")
        f.write("<hr />\n")
        f.write(database_html + "\n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>RNA type annotations</h2>\n")
        f.write("<hr />\n")
        f.write(rnatype_html + "\n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>RNAcode</h2>\n")
        f.write("<hr />\n")
        f.write(rnacode_html)
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>R-scape</h2>\n")
        f.write("<hr />\n")
        f.write(rscape_html + "\n")
        f.write("<br> \n")
        f.write("<font size='2' color='grey'>")
        f.write("    <i><a href=\"./rscape/\">[Explore R-scape results]</a></i>\n")
        f.write("</font>")
        f.write("<br> \n")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write("<h2>Full information</h2> \n")
        f.write("<hr />\n")
        f.write("<font size='2' color='grey'>")
        f.write("    <i><a href=\"file:%s.txt\">[Explore alignment file]</a></i>\n" % os.path.basename(stoali))
        f.write("</font>")
        f.write("<br>\n")
        f.write("<br>\n")
        f.write(fullinfo_html + "\n")
        f.write("</div>")
        f.write(footer)
    # HOME INFO
    f_file = aliname
    f_name = df_desc["description"][1]
    f_numseq = df_easelstats[0][0]
    f_alen = df_easelstats[0][1]
    f_avlen = df_easelstats[0][3]
    f_lenalen = df_easelstats[0][4]
    f_avid = df_easelstats[0][5]
    f_numpub = len(df_publications)
    f_numdb = len(database_df)
    f_type = str(dominant_type(df_xrefs))

    if check_rnacode(stoali):
        f_codingwarn = "Yes"

    else:
        f_codingwarn = "No"

    if check_rscape(stoali):
        f_rscape = "Yes"

    else:
        f_rscape = "No"

    infoline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (f_file,
                                                                 f_name,
                                                                 f_numseq,
                                                                 f_alen,
                                                                 f_avlen,
                                                                 f_lenalen,
                                                                 f_avid,
                                                                 f_numpub,
                                                                 f_numdb,
                                                                 f_codingwarn,
                                                                 f_rscape,
                                                                 f_type)

    return infoline


def write_homeinfo(infoline, out_tsv):
    """
    """
    with open(out_tsv, "a") as f:
        f.write(infoline)
        f.close()


def iterdir(eslalistat, hometsv, dir_path):
    """
    Makes iteration of main function in a directory containing
    directories with an alignment inside.
    """
    for folder in glob.glob(os.path.join(dir_path, '*')):
        # this part checks if there's already a generated html file,
        # so if the script crashes, it's relaunchable without
        # making a mess
        htmls = glob.glob(os.path.join(folder, "*.html"))
        if len(htmls) == 0:
            alignments = glob.glob(os.path.join(folder, "*.sto"))
            for filesto in alignments:
                shutil.copy(filesto, filesto + ".txt")
                infoline = make_html(eslalistat, filesto)
                write_homeinfo(infoline, hometsv)


def home_table(hometsv):
    browse_df = pd.read_csv(hometsv,
                            sep="\t",
                            header=None)
    browse_df.columns = [["file",
                          "name",
                          "num_seq",
                          "alen",
                          "avlen",
                          "lenalen_ratio",
                          "avid",
                          "num_pub",
                          "num_db",
                          "codingwarn",
                          "rscapewarn",
                          "dominant_type"]]
    browse_df["num_seq"] = browse_df["num_seq"].astype(int)
    browse_df["alen"] = browse_df["alen"].astype(int)
    browse_df["avlen"] = browse_df["avlen"].astype(int)
    browse_df["avid"] = browse_df["avid"].astype(int)
    browse_df["avid"] = browse_df["avid"].astype(str) + "%"
    browse_df["name"] = browse_df["name"].str.replace(r"\[subseq from\]", "")
    browse_df["path"] = browse_df["file"].str.replace(r".cl.sto", "").astype(str)
    browse_df["path"] = browse_df["path"].str.replace(r".sto", "").astype(str)
    browse_df["path"] = "./indiv_pages/" + browse_df["path"] + "/" + browse_df["file"].astype(str) + ".html"

    browse_df["file"] = "<a href=\"" + browse_df["path"] + "\">" + browse_df["file"] + "</a>"
    del browse_df["path"]
    browse_df.columns = ["Alignment",
                          "Selected description",
                          "Number of<br>sequences",
                          "Alignment<br>length",
                          "Avg. sequence<br>length",
                          "Lengths<br>ratio",
                          "Avg. id",
                          "Number of<br>publications",
                          "Number of<br>databases",
                          "RNAcode<br>warning",
                          "R-scape<br>sig.",
                          "Dominant<br>rna_type"]

    return browse_df


def home_html(homehtml, hometsv):
    """
    """
    browse_df = home_table(hometsv)
    browse_html = browse_df.to_html(header=True,
                                    index=False,
                                    escape=False,
                                    classes='sortable')
    # .. OTHER HTML
    header = """
             <html>
                   <head>
                         <title>autoRfam</title>
                         <script src="./sorttable.js"></script>
                   </head>
             """
    body = """
           <body style="font-family:'helvetica';
                        margin-top: 1%;
                        margin-bottom: 1%;
                        margin-right: 4%;
                        margin-left: 2%;"
                 link="#3366BB"
                 vlink="#663366">
           """

    style = """
            <style>
                   h1{color: #7a0606;
                      font-family: helvetica;
                      font-weight:normal;
                      font-size: 350%}
                   h2, h3 {color: #822424;
                           font-family: helvetica;
                           font-weight:normal;
                           display: inline;}
                   .df
                      th {text-align: left;
                          background-color: #822424;
                          color: white;
                          font-family:helvetica;}
                      table {border-collapse: collapse;}
                      table, th, td {border: 1px solid black;
                                     font-family: monospace;
                                     text-align: right;
                                     font-size:12px;
                                     font-weight:normal;
                                     padding:5px 10px;
                                     white-space: nowrap;
                                     border-style:solid;
                                     border-width:1px;}
                      tr:hover {background-color: #e8e5e5}

                      table.sortable th {text-align: left;
                                         background-color: #822424;
                                         color: white;
                                         font-family:helvetica;}
                                     th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {
                                        content: ' \\25B9'}
            </style>
            """

    footer = """
                    </body>
             </html>
             """

    # ....Writing HTML File
    with open(homehtml, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(style)
        f.write("\n")
        f.write("<div align='right'>\n")
        f.write("<font size='2' color='grey'>")
        f.write("[ <a href='./help.html'>help</a> ]&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;browse alignments")
        f.write("</font>\n")
        f.write("</div>\n")
        f.write("<h1>autoRfam\n")
        f.write("    <font size='5' color='grey'>\n")
        f.write("        <i>BROWSE ALIGNMENTS</i>\n")
        f.write("    </font>\n")
        f.write("</h1>\n")
        f.write("<br>\n")
        f.write(browse_html+"\n")
        f.write(footer)


def main(eslalistat, dirpath, homehtml, hometsv):
    """
    """
    iterdir(eslalistat, hometsv, dirpath)
    home_html(homehtml, hometsv)

# .........................................................................

if __name__ == '__main__':
    ESLALISTAT_PATH = sys.argv[1]
    DIR_PATH = sys.argv[2]
    homehtml = sys.argv[3]
    HOMETSV = sys.argv[4]
    main(ESLALISTAT_PATH, DIR_PATH, homehtml, HOMETSV)
