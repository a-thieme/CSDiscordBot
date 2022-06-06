import feedparser
import pandas as pd
import json

import threading


def make_json():
    out = {
        "Courses": {},
        "Professors": {
            "William Baggett": {
                "title": "Instructor",
                "email": "wbaggett@memphis.edu",
                "office": "DH 390"
            },
            "Amy Cook": {
                "title": "Assistant Professor",
                "email": "ascook@memphis.edu",
                "office": "DH 113"
            },
            "Dipankar Dasgupta": {
                "title": "Professor",
                "email": "dasgupta@memphis.edu",
                "office": "DH 333"
            },
            "Scott Fleming": {
                "title": "Associate Professor & Associate Chair",
                "email": "scott.fleming@memphis.edu",
                "office": "DH 303"
            },
            "Max Garzon": {
                "title": "Professor",
                "email": "mgarzon@memphis.edu",
                "office": "DH 325"
            },
            "Xiaolei Huang": {
                "title": "Assistant Professor",
                "email": "xhuang7@memphis.edu",
                "office": "DH 111"
            },
            "Nirman Kumar": {
                "title": "Assistant Professor",
                "email": "nkumar8@memphis.edu",
                "office": "DH 307"
            },
            "Santosh Kumar": {
                "title": "Professor",
                "email": "santosh.kumar@memphis.edu",
                "office": "DH 319"
            },
            "Weizi Li": {
                "title": "Assistant Professor",
                "email": "wli@memphis.edu",
                "office": "DH 321"
            },
            "Kriangsiri \"Top\" Malasri": {
                "title": "Instructor & Advising Coordinator",
                "email": "kmalasri@memphis.edu",
                "office": "DH 396"
            },
            "Christos Papadopoulos": {
                "title": "Professor",
                "email": "christos.papadopoulos@memphis.edu",
                "office": "N/A"
            },
            "Vinhthuy Phan": {
                "title": "Associate Professor",
                "email": "vphan@memphis.edu",
                "office": "DH 309"
            },
            "Vasile Rus": {
                "title": "Professor",
                "email": "vrus@memphis.edu",
                "office": "DH 323"
            },
            "Fatih Sen": {
                "title": "Instructor",
                "email": "fsen@memphis.edu",
                "office": "DH 301"
            },
            "Sajjan Shiva": {
                "title": "Professor",
                "email": "sshiva@memphis.edu",
                "office": "DH 335"
            },
            "Deepak Venugopal": {
                "title": "Associate Professor",
                "email": "dvngopal@memphis.edu",
                "office": "DH 317"
            },
            "Lan Wang": {
                "title": "Department Chair & Professor",
                "email": "lanwang@memphis.edu",
                "office": "DH 321"
            },
            "Thomas Watson": {
                "title": "Assistant Professor",
                "email": "thomas.watson@memphis.edu",
                "office": "DH 315"
            },
            "Myounggyu Won": {
                "title": "Assistant Professor",
                "email": "mwon@memphis.edu",
                "office": "DH 398"
            },
            "Kan Yang": {
                "title": "Assistant Professor",
                "email": "kan.yang@memphis.edu",
                "office": "DH 305"
            },
            "James Yu": {
                "title": "Instructor",
                "email": "jyu8@memphis.edu",
                "office": "DH 320"
            },
            "Xiaofei Zhang": {
                "title": "Assistant Professor",
                "email": "xiaofei.zhang@memphis.edu",
                "office": "DH 318"
            }
        }
    }
    df = make_df()
    for row in df.iterrows():
        row = row[1]

        # crn stuff
        Crn = row['CRN']

        # crn is 'nan'
        if type(Crn) != str:
            continue

        # headers I think
        if Crn == "CRN":
            continue

        # subject headings
        if not Crn.isdigit():
            continue

        if row['Subj'] + str(row['Crse']) not in out['Courses']:
            out['Courses'][row['Subj'] + str(row['Crse'])] = {}

        out['Courses'][row['Subj'] + str(row['Crse'])]['name'] = row['Title']
        out['Courses'][row['Subj'] + str(row['Crse'])]['hours'] = row['Cred']
        if 'sections' not in out['Courses'][row['Subj'] + str(row['Crse'])]:
            out['Courses'][row['Subj'] + str(row['Crse'])]['sections'] = {}

        out['Courses'][row['Subj'] + str(row['Crse'])]['sections'][row['Sec']] = {
            'location': row['Location'],
            'instructor': row['Instructor'],
            'days': row['Days'],
            'time': row['Time'],
            'rss': {
                'id': 'N/A',
                'token': 'N/A'
            }
        }

        if 'prerequisites' not in out['Courses'][row['Subj'] + str(row['Crse'])]:
            out['Courses'][row['Subj'] + str(row['Crse'])]['prerequisites'] = []

        prof = row['Instructor'].split('(P)')[0].strip()
        if prof == 'TBA' or prof not in out['Professors']:
            out['Professors'][prof] = {
                'title': 'normie instructor/professor',
                'email': 'someone@memphis.edu',
                'office': 'prolly not in dunn hall'
            }

    with open('output.json', 'w') as f:
        f.writelines(json.dumps(out, indent=4))


# This is a sample Python script.
def rss():
    something = feedparser.parse(
        'https://memphis.instructure.com/feeds/announcements/enrollment_apVbRwKfN5CpQMOirXwniGPEefE0M6QcR1qvyrRX.atom')
    # for i in range(len(something)):
    #     print(something.entries[i])
    with open('output.html', 'w') as f:
        f.write("<html><body>")
        for i in something.entries:
            # print(i.content[0].value)
            f.write(i.content[0].value)
        f.write("</body></html>")


def strip_post():
    s = 'curl "https://ssb.bannerprod.memphis.edu/prod/bwskfcls.P_GetCrse_Advanced" -X POST -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br" -H "Referer: https://ssb.bannerprod.memphis.edu/prod/bwskfcls.P_GetCrse_Advanced" -H "Content-Type: application/x-www-form-urlencoded" -H "Origin: https://ssb.bannerprod.memphis.edu" -H "DNT: 1" -H "Connection: keep-alive" -H "Cookie: TESTID=set; SESSID=NTBZSFNMNzQ3NTQ4; IDMSESSID=FBEF66F67444D5BB275B952383DE5376B380B406A171D0419741F56A742FABEA36731F318065A3FC01FCA939E3181CE7274A5250DC83889043AD4FC6A8198487" -H "Upgrade-Insecure-Requests: 1" -H "Sec-Fetch-Dest: document" -H "Sec-Fetch-Mode: navigate" -H "Sec-Fetch-Site: same-origin" -H "Sec-GPC: 1" --data-raw "rsts=dummy&crn=dummy&term_in=202210&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=AAAS&sel_subj=ACAD&sel_subj=ACCT&sel_subj=ADVR&sel_subj=AERO&sel_subj=AGRI&sel_subj=ALHS&sel_subj=ANTH&sel_subj=ARAB&sel_subj=ARCH&sel_subj=ARMY&sel_subj=ART&sel_subj=ARTH&sel_subj=ASTL&sel_subj=ASTR&sel_subj=AUSP&sel_subj=AVIA&sel_subj=BA&sel_subj=BINF&sel_subj=BIOL&sel_subj=BIOM&sel_subj=BMGT&sel_subj=BUED&sel_subj=BUSN&sel_subj=CANV&sel_subj=CAS&sel_subj=CCFA&sel_subj=CDFS&sel_subj=CERI&sel_subj=CHEM&sel_subj=CHIN&sel_subj=CISP&sel_subj=CITC&sel_subj=CIVL&sel_subj=CJA&sel_subj=CJUS&sel_subj=CLAS&sel_subj=COBH&sel_subj=COL&sel_subj=COM&sel_subj=COMM&sel_subj=COMP&sel_subj=COUN&sel_subj=CPSY&sel_subj=CRMJ&sel_subj=CRMM&sel_subj=CSC&sel_subj=CSCI&sel_subj=CST&sel_subj=DANC&sel_subj=ECED&sel_subj=ECON&sel_subj=EDAD&sel_subj=EDCI&sel_subj=EDPR&sel_subj=EDSV&sel_subj=EDU&sel_subj=EDUC&sel_subj=EECE&sel_subj=ELC&sel_subj=ELED&sel_subj=ELPA&sel_subj=EMGT&sel_subj=ENGL&sel_subj=ENGR&sel_subj=ENTC&sel_subj=ENVR&sel_subj=EPLC&sel_subj=ESCI&sel_subj=ESMS&sel_subj=ET&sel_subj=EXSS&sel_subj=FIR&sel_subj=FREN&sel_subj=FTHT&sel_subj=GEOG&sel_subj=GEOL&sel_subj=GERM&sel_subj=GREK&sel_subj=HADM&sel_subj=HCL&sel_subj=HEBR&sel_subj=HETH&sel_subj=HIAD&sel_subj=HIST&sel_subj=HIT&sel_subj=HLSC&sel_subj=HMSE&sel_subj=HPRM&sel_subj=HPRO&sel_subj=HPSS&sel_subj=HSC&sel_subj=HTL&sel_subj=HUM&sel_subj=ICL&sel_subj=IDES&sel_subj=IDT&sel_subj=IIS&sel_subj=INFS&sel_subj=INTL&sel_subj=IST&sel_subj=ITAL&sel_subj=JAPN&sel_subj=JDST&sel_subj=JOUR&sel_subj=JRSM&sel_subj=KORE&sel_subj=LALI&sel_subj=LATN&sel_subj=LAW&sel_subj=LBRY&sel_subj=LDPS&sel_subj=LDSP&sel_subj=LEAD&sel_subj=LEGL&sel_subj=LING&sel_subj=LIST&sel_subj=LITL&sel_subj=MATH&sel_subj=MDT&sel_subj=MECH&sel_subj=MGMT&sel_subj=MIS&sel_subj=MKED&sel_subj=MKT&sel_subj=MKTG&sel_subj=MRCH&sel_subj=MUAP&sel_subj=MUHL&sel_subj=MUID&sel_subj=MUS&sel_subj=MUSE&sel_subj=MUTC&sel_subj=NAVY&sel_subj=NURS&sel_subj=NUTR&sel_subj=PADM&sel_subj=PBRL&sel_subj=PETE&sel_subj=PHED&sel_subj=PHIL&sel_subj=PHYS&sel_subj=PLAN&sel_subj=PM&sel_subj=POLI&sel_subj=POLS&sel_subj=PORT&sel_subj=PRST&sel_subj=PS&sel_subj=PSCI&sel_subj=PSY&sel_subj=PSYC&sel_subj=PTMA&sel_subj=PUBH&sel_subj=QM&sel_subj=RLGN&sel_subj=RUSS&sel_subj=SCED&sel_subj=SCMS&sel_subj=SLC&sel_subj=SLS&sel_subj=SOAA&sel_subj=SOC&sel_subj=SOCI&sel_subj=SPAN&sel_subj=SPED&sel_subj=SPRT&sel_subj=SUAP&sel_subj=SW&sel_subj=SWRK&sel_subj=TEAE&sel_subj=TEAS&sel_subj=TECH&sel_subj=TELC&sel_subj=THEA&sel_subj=UAPP&sel_subj=UNHP&sel_subj=UNIV&sel_subj=WEB&sel_subj=WEBD&sel_subj=WEBT&sel_subj=WMST&sel_subj=WGST&sel_crse=&sel_title=&sel_insm="%"25&sel_from_cred=&sel_to_cred=&sel_camp="%"25&sel_levl="%"25&sel_ptrm="%"25&sel_instr="%"25&sel_attr="%"25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a&SUB_BTN=Section+Search&path=1"'
    s = s.replace('-H', '\n-H')
    s = s.replace('&', '\n&')
    s = s.replace('--data-raw "', '\n--data-raw "\n')
    print(s)


def strip_raw():
    output = []
    with open('AllClasses-raw.html', 'r') as f:
        in_table = False
        first_group = False
        hold = ''
        for line in f:
            if in_table:
                if not first_group and 'colgroup' in line:
                    hold = line
                    first_group = True
                    continue
                if '</table>' in line:
                    output.append('<tr>')
                    output.append(hold)
                    output.append('<tr>')
                    in_table = False
                output.append(line)
            else:
                if 'datadisplaytable' in line:
                    output.append(line)
                    in_table = True

    # output.remove('<th colspan="26" class="ddtitle" scope="colgroup">AAAS Afrcn and Afrcn-Amer Stds</th>\n')
    return output


term = 202210


def create_tables(input_df):
    subject = pd.DataFrame()
    course = pd.DataFrame()
    section = pd.DataFrame()
    instructor = pd.DataFrame()
    taught_by = pd.DataFrame()

    Course = ['Subj', 'Crse', 'Cred', 'Title']
    Section = ['CRN', 'Subj', 'Crse', 'Sec', 'Time', 'Days', 'Location', 'Date (MM/DD)', 'Cap', 'Act', 'Rem',
               'WL Act', 'Attribute']
    at = ''
    rows = input_df.iterrows()
    for row in rows:
        row = row[1]

        # crn stuff
        Crn = row['CRN']

        # crn is 'nan'
        if type(Crn) != str:
            continue

        # headers I think
        if Crn == "CRN":
            continue

        # subject headings
        if not Crn.isdigit():
            splitted = str(Crn).split(' ', 1)
            entry = [splitted[0], splitted[1]]
            if entry[0] == 'CIS':
                entry[0] = 'CISP'
            # if entry[0] not in something.values:
            #     something = something.append(pd.Series(entry, index=['subj', 'name']), ignore_index=True)
            subject = subject.append(pd.Series(entry, index=['subj', 'name']), ignore_index=True)
            continue

        if len(str(row['Attribute'])) > len(at):
            at = str(row['Attribute'])

        # fixme

        # Instructor and teaches
        for inst in row['Instructor'].split(','):
            inst = inst.strip()
            if 'TBA' in inst:
                continue
            is_primary = '(P)' in inst
            if is_primary:
                inst = inst.replace('(P)', '').strip()
            instructor = instructor.append(
                pd.Series([inst], index=['name']), ignore_index=True)
            taught_by = taught_by.append(
                pd.Series([is_primary, inst, row['CRN']],
                          index=['is_primary', 'instructor', 'crn']),
                ignore_index=True)
        # course table
        course = course.append(pd.Series([row[key] for key in Course], index=['subj', 'num', 'credits', 'title']),
                               ignore_index=True)
        section = section.append(
            pd.Series([row[key] for key in Section] + [term], index='crn subj num sec_num time days location date '
                                                                    'cap act rem wl_acting attribute term_id'.split(
                ' ')),
            ignore_index=True)

    # remove dupes for primary keys
    course = course.drop_duplicates(subset=['subj', 'num'])
    section = section.drop_duplicates(subset=['subj', 'num', 'sec_num'])
    section = section.drop_duplicates(subset=['crn'])
    subject = subject.drop_duplicates(subset=['subj'])
    taught_by = taught_by.drop_duplicates()
    instructor = instructor.drop_duplicates()

    # # output for viewing in excel
    # with pd.ExcelWriter('output.xlsx') as writer:
    #     course.to_excel(writer, sheet_name='course')
    #     section.to_excel(writer, sheet_name='section')
    #     instructor.to_excel(writer, sheet_name='instructor')
    #     subject.to_excel(writer, sheet_name='subject')
    #     taught_by.to_excel(writer, sheet_name='taught_by')

    # eventually, this might return all the tables
    from sqlalchemy import create_engine
    # engine = create_engine("mysql+pymysql://adamt:yummy@135.148.40.213:3306/university")
    engine = create_engine("mysql+pymysql://root:something@localhost:3306/university")
    con = engine.connect()

    instructor.to_sql('instructor', index=False, con=con, if_exists='append')
    subject.to_sql('subject', con=con, index=False, if_exists='append')
    course.to_sql('course', con=con, index=False, if_exists='append')
    pd.DataFrame({
        'term_id': [202210],
        'semantic': ['Spring 2022']
    }).to_sql('term', con=con, index=False, if_exists='append')
    section.to_sql('section', con=con, index=False, if_exists='append')
    taught_by.to_sql('taught_by', con=con, index=False, if_exists='append')

    return subject


def make_df():
    with open('skimmed.html', 'w') as f:
        f.writelines(strip_raw())
    file = open("skimmed.html", "r")
    df = pd.read_html(file)[-1]
    return df


def master_excel_output(input_df):
    input_df.to_excel('master.xlsx')


if __name__ == '__main__':
    create_tables(make_df())
    # make_json()

    print()
