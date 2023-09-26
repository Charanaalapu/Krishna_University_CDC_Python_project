from flask import Flask, request,render_template
import pandas as pd
import os
import json
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
      return render_template('index.html')

webbrowser.open("http://127.0.0.1:5000")

@app.route('/', methods=['POST','GET'])
def process():
    if request.method=='POST':
          
        clg_code=request.form.get('clg_code')
        
        pth ="D:\\Project\\"
        f_clgmaster= pth + "college_master_csv.csv"
        f_crsmaster= pth + "course_master_csv.csv"
        f_clgadmaster= pth + "college_admission_master_csv.csv"
        f_clgcrsmaster= pth + "college_course_master_csv.csv"
        f_clgfeedemand= pth + "college_fee_demand_csv.csv"
        f_clgfdemand_total = pth + "college_fee_demand_total_csv.csv"
        r_report= pth + "f_report.txt"
        r_clgcrs = pth + "r_clgcrs.txt"
        r_clgad = pth + "r_clgad.txt"
        r_fdemand = pth + "r_fdemand.txt"

        ##Open a file for output
        #f_output = open(f_output,"w")#append mode

        #Rading College master file in df
        df1=pd.read_csv(f_clgmaster)
        df_clgmaster= pd.DataFrame(df1)
        df_clgmaster.set_index('college_code')

        ## Reading Course Master file
        df2=pd.read_csv(f_crsmaster)
        df_crsmaster= pd.DataFrame(df2)
        df_crsmaster.set_index('course_code')

        #Reading College admisions Master file
        df2=pd.read_csv(f_clgadmaster)
        df_clgadmaster= pd.DataFrame(df2)
        df_clgadmaster.set_index('college_code')

        #Reading College course Master file
        df2=pd.read_csv(f_clgcrsmaster)
        df_clgcrsmaster= pd.DataFrame(df2)
        df_clgcrsmaster.set_index('college_code')

        #Reading College fee demand file   ## Not required here in side program is used

        #df2=pd.read_csv(f_clgfeedemand)
        #df_clgfeedemand= pd.DataFrame(df2)
        #df_clgfeedemand.set_index('college_code')

        # Reading fee demand total  ## Not required here in side program is used
        df2=pd.read_csv(f_clgfdemand_total)
        df_clgfeedemand_total= pd.DataFrame(df2)
        df_clgfeedemand_total.set_index('college_code')

        # Report Generation
        os.system("cls")

        #sys.stdout = open(f_output, "w")
        o_report=open(r_report,'w')
        o_clgcrs = open(r_clgcrs,"w")
        o_clgad = open(r_clgad,"w")
        o_fdemand = open(r_fdemand,"w")

        #o_fdemand_total = open(f_clgfdemand_total,"a") not required
        ###   Readng admission data 

        # 1. Set academic year
        academic_year= json.loads("2022")

        # 2. Read college Code
        code =clg_code
        
        college_code= json.loads(code) # to convert as object
        #s2="\n\tCollege Code: %d"+ str(college_code)
        #f_output.write(s2)

        # Setting the path for saving collegewise report
        report_pth="D:\\Project\\Fee_Reports\\"
        r_final_report = report_pth + "r" +str(code)+ "_final_report"
        # print(" r Path=",r_final_report)

        # Extracting college master data
        clgf = df_clgmaster[ df_clgmaster['college_code'] == college_code ]
        college_jvdid=clgf['college_jvdid']
        college_name = clgf['college_name']
        # clg report
        s1 = "\n                       Krishna Unversity"
        s2 = "\n                    College Fee Demand Notice"
        s3= "\nCollege code: " + str(college_code)
        s4 ="\tCollege jvdid: " +  college_jvdid.to_string(index=False)
        s5 ="\n College name: " + college_name.to_string(index =False)

        # College crs             
        o_report.write(s1)
        o_report.write(s2)
        o_report.write(s3)
        o_report.write(s4)
        o_report.write(s5)
        st ="\n\t\t College Course Details"
        o_clgcrs.write(st)
        st ="\ncoure\t    c_code  c_id  spl.   sub1      sub2         sub3      \t\tintake"
        o_clgcrs.write(st)

        # college admissions
        st= "\nyear wise admissions\nclg_code crs_id intake 1st\t2nd\t3rd\t  4th   5th"
        o_clgad.write(st)

        # Fee demand
        st ="\nclg_code crs_cd crs_id  aff_fee\trru1_fee  rru2+_fee  iut_fee  yf_fee"
        o_fdemand.write(st)

        # Extrating college course details
        clgcrsf=df_clgcrsmaster[ df_clgcrsmaster['college_code'] == college_code]
        ncourses = len(clgcrsf.axes[0])

        # Get course ids for each course in college list
        ttcrs = clgcrsf['course_id']
        ttcrs_ind =clgcrsf.axes[0]

        #print("ttcrs\n",ttcrs_ind)
        # Reading College Course wise admission  details
        clgadf = df_clgadmaster[ df_clgadmaster['college_code'] == college_code]
        ncrsads= len(clgadf.axes[0])               
        ttcrsad = clgadf['course_id']
        ttcrsad_ind = clgadf.axes[0]

        ##Total fee demand initializatiol
        total_affl_fee=0
        total_rru_first_fee=0
        total_rru_secondplus_fee=0
        total_iut_fee=0
        total_yf_fee=0
        total_sp_fee=1200
        total_insp_fee=10000
        grand_total_fee=0

        # print("\n\tncourse s= :", ncourses)
        for c in range(ncourses):
            clgcrsrow= clgcrsf.iloc[c] # working college 258
            clgcrsrow.fillna('*')
            #print(clgcrsrow)
            course_id= int(clgcrsrow['course_id'])
            course_code = int(clgcrsrow['course_code'])
            clgadrow = clgadf[ clgadf['course_id'] == course_id]
            clgadrow.fillna(0)
            #print(clgcrsrow['course_id'] ) #check point
            #print(clgadrow['course_id'] ) #check point
            crsrow = df_crsmaster[ df_crsmaster['course_code'] ==course_code]
            crsrow.fillna(0)
            #print(crsrow)  # check point

            #Extracting course details from course master
            cn = crsrow['course_name']
            course_name = cn.to_string(index=False)
            caf = crsrow['course_affiliation_fee']
            course_affiliation_fee = int(caf)
            rru1 = crsrow['student_rru_fee_first_year']
            student_rru_fee_first_year = int(rru1)
            rru2 = crsrow['student_rru_fee_secondplus']
            student_rru_fee_secondplus = int(rru2)
            iut = crsrow['student_iut_fee']
            student_iut_fee = int(iut)
            yff = crsrow['student_yf_fee']
            student_yf_fee = int(yff)
            cd = crsrow['course_duriation']
            course_duration = int(cd)

            #Extracting college course  details from college course  master
            ci = clgcrsrow['course_intake']
            course_intake = int(ci)
            course_spl= clgcrsrow['course_spl']
            if pd.isna(course_spl):
                    course_spl="***"             
            course_subject1= clgcrsrow['course_subject1']
            if pd.isna(course_subject1):
                    course_subject1="***"
            course_subject2= clgcrsrow['course_subject2']
            if pd.isna(course_subject2):
                    course_subject2="***"
            course_subject3= clgcrsrow['course_subject3']
            if pd.isna(course_subject3):
                    course_subject3="***"
            ys = clgcrsrow['year_of_start']
            year_of_start = int(ys)

            # Extarcting course wise admission details from college admission master      
            st1 = clgadrow['student_strength_first_year']
            #print(len(st1.axes[0]))
            student_strength_first_year = int(st1)
            year_count = 1
            if (year_count < course_duration):
                    st2 = clgadrow['student_strength_second_year']
                    student_strength_second_year = int(st2)
            else:
                    student_strength_second_year =0
            year_count = year_count +1
            if (year_count < course_duration):
                    st3 = clgadrow['student_strength_third_year']
                    student_strength_third_year = int(st3)
            else:
                student_strength_third_year=0  
            year_count = year_count +1
            if (year_count < course_duration):
                    st4 = clgadrow['student_strength_fourth_year']
                    student_strength_fourth_year = int(st4)
            else:
                student_strength_fourth_year =0 
            year_count = year_count +1
            if (year_count < course_duration):
                    st5 = clgadrow['student_strength_fifth_year']
                    student_strength_fifth_year = int(st5)
            else:
                    student_strength_fifth_year =0
            year_count = year_count +1 

            # Caliculatinf  various fee demand                                 
            if  (len(clgadrow.axes[0]) > 0 ):   # if course has admissions              
                    #  affiliation fee demand
                    stad_percent =  ( student_strength_first_year / course_intake )*100
                    # print(stad_percent)
                    if ( stad_percent >=0 and stad_percent <= 25 ):
                        course_affiliation_fee_payable  =  course_affiliation_fee * 0.25
                    elif  ( stad_percent > 25 and stad_percent <= 50 ):
                        course_affiliation_fee_payable  =  course_affiliation_fee * 0.5
                    else:
                        course_affiliation_fee_payable  =  course_affiliation_fee
                    # rru fee demand          
                    student_rru_fee_first_year_payable = student_strength_first_year * student_rru_fee_first_year
                    students_secondplus = ( student_strength_second_year + student_strength_third_year + student_strength_fourth_year + student_strength_fifth_year )
                    student_rru_fee_secondplus_payable = students_secondplus * student_rru_fee_secondplus
                    # iut fee demand
                    total_students = student_strength_first_year + students_secondplus
                    student_iut_fee_payable = total_students * student_iut_fee
                    # yf demand
                    student_yf_fee_payable = total_students * student_yf_fee
            else: # if course has no admissions
                    course_affiliation_fee_payable  =  course_affiliation_fee * 0.25
                    student_rru_fee_first_year_payable =0
                    student_rru_fee_secondplus_payable = 0
                    student_iut_fee_payable = 0
                    student_yf_fee_payable =0

            # appending data into college fee demand
            dist = { 'college_code' : [college_code], 'academic_year' : [academic_year], 'course_code' : [course_code],'course_id' :[course_id], 'course_affiliation_fee_payable' : [course_affiliation_fee_payable], 'student_rru_fee_first_year_payable' : [student_rru_fee_first_year_payable], 'student_rru_fee_secondplus_payable' : [student_rru_fee_secondplus_payable], 'student_iut_fee_payable' : [student_iut_fee_payable],'student_yf_fee_payable' : [student_yf_fee_payable] } 
            new_row=pd.DataFrame(dist)
            new_row.set_index('course_code')

            #Rading College fee demand file
            df2=pd.read_csv(f_clgfeedemand)
            df_clgfeedemand= pd.DataFrame(df2)
            df_clgfeedemand.set_index('college_code')
            #print(df_clgfeedemand.axes[0]) # check point
            #print(df_clgfeedemand.axes[1])  # check point
            dfnew= df_clgfeedemand._append(new_row)
            dfnew.set_index('course_code')
            dfnew.to_csv(f_clgfeedemand, index=False)
            total_affl_fee  +=  course_affiliation_fee_payable
            total_rru_first_fee +=  student_rru_fee_first_year_payable
            total_rru_secondplus_fee += student_rru_fee_secondplus_payable
            total_iut_fee  +=   student_iut_fee_payable
            total_yf_fee +=   student_yf_fee_payable

            #total_sp_fee += 0          
            #total_insp_fee += 0
            # report generation college course details     
            #st="\n"  + course_name + "\t" + str(course_code) + "\t" + str(course_id) + "\t" + course_spl +  "\t" + course_subject1 + "\t      " + course_subject2 + "\t         "  + course_subject3 + "                \t" + str(course_intake)
            #print(course_name, course_code, course_id, course_spl, course_subject1, course_subject2, course_subject3, course_intake)
            st= "\n{:<10s} {:4d} {:4d} {:10s} {:10s} {:10s} {:10s} \t{:5d} ".format(course_name, course_code, course_id, course_spl, course_subject1, course_subject2, course_subject3, course_intake)
            o_clgcrs.write(st)

            # report generation college admission detals
            #st= "\n" + str(course_code) + "\t" + str(course_id) + "\t"+ str(course_intake) + "\t" + str(student_strength_first_year) + "\t" + str(student_strength_second_year) + "\t" + str(student_strength_third_year) + "\t" + str(student_strength_fourth_year)  + "\t" + str(student_strength_fifth_year)
            st= "\n{:6d} {:6d} {:6d}{:6d}{:6d}{:6d}{:6d}{:6d}".format(course_code, course_id, course_intake, student_strength_first_year, student_strength_second_year, student_strength_third_year, student_strength_fourth_year, student_strength_fifth_year)
            o_clgad.write(st)

            #report generation fee demand
            #st="\n" + str(college_code) +" \t    "+  str(course_code) +" \t    "+ str(course_id) +" \t    "+  str(course_affiliation_fee_payable) +" \t    "+ str(student_rru_fee_first_year_payable) +" \t    "+  str(student_rru_fee_secondplus_payable) +" \t    "+ str(student_iut_fee_payable) +" \t    "+ str(student_yf_fee_payable)
            st="\n{:6d} {:6d} {:6d}{:10.2f}{:10d}{:10d}{:10d}{:10d}".format(college_code, course_code, course_id, course_affiliation_fee_payable, student_rru_fee_first_year_payable, student_rru_fee_secondplus_payable, student_iut_fee_payable, student_yf_fee_payable)
            o_fdemand.write(st)

        # appending data into college fee demand total
        grand_total_fee= total_affl_fee + total_rru_first_fee + total_rru_secondplus_fee + total_iut_fee + total_yf_fee + total_sp_fee + total_insp_fee
        dist = { 'college_code' : [college_code], 'academic_year' : [academic_year], 'course_affiliation_fee_payable' : [total_affl_fee], 'student_rru_fee_first_year_payable' : [total_rru_first_fee], 'student_rru_fee_secondplus_payable' : [total_rru_secondplus_fee], 'student_iut_fee_payable' : [total_iut_fee],'student_yf_fee_payable' : [total_yf_fee],'college_sports_fee' : [total_sp_fee] , 'college_insp_fee' : [total_insp_fee]} 
        new_row=pd.DataFrame(dist)
        new_row.set_index('college_code')

        #Rading College fee demand file
        df2=pd.read_csv(f_clgfdemand_total)
        df_clgfdemand_total= pd.DataFrame(df2)
        df_clgfdemand_total.set_index('college_code')
        #print(df_clgfeedemand_total.axes[0]) # check point
        #print(df_clgfeedemand_total.axes[1])  # check point
        dfnew= df_clgfdemand_total._append(new_row)
        dfnew.set_index('college_code')
        dfnew.to_csv(f_clgfdemand_total, index=False)

        # closing files
        o_report.close()
        o_clgcrs.close()
        o_clgad.close()
        o_fdemand.close()

        #merging files
        data1 = data2 = data3 = data4 = data= " "
        with open(r_report) as fd:
            data1= fd.read()
        with open(r_clgcrs) as fd:
            data2= fd.read()
        with open(r_clgad) as fd:
            data3= fd.read()
        with open(r_fdemand) as fd:
            data4= fd.read()

        # Wrting total fee details into final report file
        data5 ="\nTOTAL FEE PAYABLE :\nclg_code  aff_fee\t    rru1_fee  rru2+_fee  iut_fee\tyf_fee  sports_fee  insp_fee"
        data6 ="\n{:6d} {:10.2f}{:10d}{:10d}{:10d}{:10d} {:10d} {:10d} \n\nGrand Total demand: {:10.2f}".format(college_code, total_affl_fee, total_rru_first_fee, total_rru_secondplus_fee, total_iut_fee, total_yf_fee,total_sp_fee, total_insp_fee, grand_total_fee)
        ## adding Totals
        data += "\n"
        data += data1
        data += "\n"
        data += data2
        data += "\n"
        data += data3
        data += "\n"
        data += data4
        data +="\n"
        data += data5
        data +="\n"
        data += data6
        data += "\n"

        # adding totals:
        with open(r_final_report, 'w') as fp:
            fp.write(data)
    return render_template('index.html')

if __name__ == '__main__':
      app.run(debug=True)