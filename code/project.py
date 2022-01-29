import pandas as pd
from pandas.core.tools.numeric import to_numeric
import psycopg2
import streamlit as st
from configparser import ConfigParser

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data,columns=column_names)

    return df
st.sidebar.title("Select your account type!")
r=st.sidebar.radio("",('Employee','User'))
ph = st.empty()
if r=='Employee':
    st.subheader("Ticket count according to Users")
    sql_user_ids="select u_id from users;"
    
    try:
        user_ids= query_db(sql_user_ids)["u_id"].tolist()
        user_id = st.selectbox("Choose your id", user_ids)
    except:
     st.write("Sorry! something went wrong")
    
    if user_id:
        sql_ticket=f"""
            Select U.u_id as id ,U.name_is as name,count(T.ticket_id) as tickets
            from users U,ticket T 
            WHERE U.u_id = T.u_id AND T.u_id='{user_id}'
            group by U.u_id;"""
        
        
        try:
            d=query_db(sql_ticket)
            if d.empty:
                st.write(
                    f" {user_id} has not done any bookings."
                    )
            else:
                st.dataframe(d)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
    
    
    
    st.text("Which non screening movies date of release and genre wyou want to retrieve ")
    st.subheader("Genre & publish date of non screeening movies")

    #nonscm=cur.execute("((select M.m_name from moviepool M) EXCEPT (select scm.m_name from screeningmovie scm)); ")
    sql_query1=query_db("""select M.m_name
    from Moviepool M
    EXCEPT
    select scm.M_name
    from screeningmovie scm;""")["m_name"].tolist()

    try:
        selected_movie_q1=st.selectbox("Select movies whose genre and release you want to know",sql_query1)
        
    except:
        st.write("Sorry! something went wrong")
    else:
        if selected_movie_q1:
            try:
                sqlq2=f"""select X.m_name, M1.genre,M1.publish,M1.duration 
                from ((select M.m_name,M.movie_id from moviepool M) 
                EXCEPT 
                (select scm.m_name,scm.movie_id from screeningmovie scm))X, moviepool M1 
                where X.m_name= '{selected_movie_q1}'
                and X.movie_id=M1.movie_id;"""
            except :
                st.write("Sorry!")
            else:
                #try:
                df1=query_db(sqlq2)
                st.dataframe(df1)
    
    st.subheader("Movies according to Genres")
    sql_query4=query_db(""" select genre, count(*) as genre_count
    from moviepool
    group by genre;""")["genre"].to_list()
    try:
        selected_genre=st.selectbox("Select the genre to view movies according to genres",sql_query4)
    except:
        st.write("OOPS! SOMETHINGS NOT RIGHT, THINK AGAIN , BETTER LUCK NEXT TIME")
    else:
        if selected_genre:
            try:
                sqlq4=f"""select m_name
                from moviepool
                where genre='{selected_genre}';"""

            except:
                st.write("oops!")
            else:
                df3=query_db(sqlq4)
                st.dataframe(df3)            
    
    st.subheader(" See User's Ticket Information")
    sql_q5=query_db("select distinct t.u_id from ticket t;")["u_id"].tolist()
    try:
        select5=st.selectbox("SELECT the User Id to seee their booking details",sql_q5)
    except:
        st.write("OOPS!")
    else:
        if select5:
            try:
                sql5=f"""select t.ticket_id,t.seat_id,t.sc_id,t.u_id,scm.m_name,u.name_is
                from screeningmovie scm, ticket t,users u
                where t.scm_id=scm.scm_id
                and u.u_id=t.u_id  AND t.u_id='{select5}';"""
            except:
                st.write("OOPS!")
            else:
                df4=query_db(sql5)
                st.dataframe(df4)
    st.subheader("Emplooyess acess to Screen")
    sql_q6=query_db("select  distinct e.e_name from screeningmovie scm ,employee e where scm.emp_id=e.emp_id order by e.e_name;")
    try:
        select_ename=st.selectbox("Select employee to check the number of their screen access",sql_q6)
    except:
        st.write("oops!")
    else:
        if select_ename:
            try:
                sql6=f"""select e.e_name, count(scm.sc_id) as Total_count
                from screeningmovie scm,employee e
                where e.emp_id=scm.emp_id
                and e.e_name='{select_ename}'
                group by e.e_name
                order by e.e_name; """
            except:
                st.write("oops!")
            else:
                df5=query_db(sql6)
                st.dataframe(df5)

    
elif r=='User':
    b = st.radio("search movie by",('genre','Time shows'))
    if b=='Time shows':
        st.title("movies according to shows")
        mtime = st.select_slider(
        'movie shows time range ',
        options=['morning shows', 'afternon shows', 'evening shows', 'night shows'])
        if mtime=="morning shows":
            scm_query="select distinct scm_id,m_name, starting  from screeningmovie where  starting > '06:00:00' and starting < '12:00:00' order by starting;"
    #scm_query="select distinct m_name from screeningmovie sm,avialable_seat am where sm.sc_id = am.sc_id;"
        elif mtime=="afternon shows":
            scm_query="select distinct scm_id,m_name, starting from screeningmovie where starting > '12:00:00' and starting < '16:00:00' order by starting;"
        elif mtime=="evening shows":
            scm_query="select distinct scm_id,m_name, starting from screeningmovie where starting > '16:00:00' and starting < '23:00:00' order by starting;"
        elif mtime=="night shows":
            scm_query="select distinct scm_id,m_name, starting from screeningmovie where starting < '06:00:00' Union select distinct scm_id,m_name, starting from screeningmovie sm where starting > '23:00:00';"
        try:
            scm_names= query_db(scm_query)#.to_string(header=False, index=False)
            scm_names['starting'] = scm_names['starting'].astype(str)
            st.dataframe(scm_names)
            scm_id = st.selectbox("select movie",scm_names)
        except:
            st.write("Sorry! something went wrong")
    elif b=='genre':
        st.title("movie according genre")
        
        sql_g=f"""
            Select distinct genre from moviepool m,screeningmovie scm 
            WHERE scm.movie_id=m.movie_id;"""
        try:
            g_sels = query_db(sql_g)["genre"].tolist()
            g_sel= st.selectbox("Genres",g_sels)
        except:
            st.write("Sorry! Something went wrong with your query, please try again.")
        scm_query=f"select distinct scm_id,scm.m_name, starting from moviepool m,screeningmovie scm WHERE scm.movie_id=m.movie_id and m.genre='{g_sel}';"
        try:
            scm_names= query_db(scm_query)#.to_string(header=False, index=False)
            scm_names['starting'] = scm_names['starting'].astype(str)
            st.dataframe(scm_names)
            scm_id = st.selectbox("select movie",scm_names)
        except:
            st.write("Sorry! something went wrong")


    if_query=f"""select count(seat_id) from seats where seat_id not in(
                select s.seat_id from seats s, screeningmovie scm, ticket t 
                where t.scm_id = scm.scm_id and scm.sc_id= s.sc_id and t.seat_id = s.seat_id
                and scm.scm_id='{scm_id}')
                and sc_id in (select s.sc_id from seats s, screeningmovie scm
                where scm.sc_id= s.sc_id 
                and scm.scm_id='{scm_id}');"""
    total_query=f"""select count(seat_id) from seats where sc_id in (select s.sc_id from seats s, screeningmovie scm
                where scm.sc_id= s.sc_id 
                and scm.scm_id='{scm_id}')"""
    try:
        if_check= query_db(if_query).loc[0].iat[0]
        total_query= query_db(total_query).loc[0].iat[0]
        total = int(total_query)
        check = int(if_check)
        if if_check > 0:
            sc_query=f"""select sc_id from screeningmovie where scm_id='{scm_id}'"""
            sc_ids= query_db(sc_query)["sc_id"].tolist()
            sc_id = st.selectbox("This selected movie with the previously shown startigntime is in in this screen ",sc_ids)
            
        else:
            st.info('sorry all seats are reserved for this shoe please reserve other show')
    except:
     st.write("Sorry! something went wrong")

    seat_query=f"""select seat_id as seats from seats where seat_id not in(
                select s.seat_id from seats s, screeningmovie scm, ticket t 
                where t.scm_id = scm.scm_id and scm.sc_id= s.sc_id and t.seat_id = s.seat_id
                and scm.scm_id='{scm_id}')
                and sc_id in (select s.sc_id from seats s, screeningmovie scm
                where scm.sc_id= s.sc_id 
                and scm.scm_id='{scm_id}');"""
    
    try:
          seat_ids= query_db(seat_query)
          st.info(f'remaining seats {check} out of {total}')
          st.dataframe(seat_ids)
          
    except:
          st.write("Sorry! something went wrong")

    st.subheader(f"My tickets information")
    sql_user_ids="select u_id from users;"
    try:
        user_ids= query_db(sql_user_ids)["u_id"].tolist()
        user_id = st.selectbox("Choose your id", user_ids)
    except:
     st.write("Sorry! something went wrong")
   
    if user_id:
        sql_ticket=f"""
            Select U.u_id as id ,U.name_is as name,count(T.ticket_id) as tickets
            from users U,ticket T 
            WHERE U.u_id = T.u_id AND T.u_id='{user_id}'
            group by U.u_id;"""
        sql_ticket_u=f"""
           select u.name_is as Name, scm.m_name as Movie, 
            t.sc_id as Screen,t.seat_id as Seat,scm.starting as ShowTime, 
            m.duration as Duration_in_minutes,s.price as price from 
            users u, screeningmovie scm, ticket t, moviepool m, seats s
            where u.u_id = t.u_id and t.scm_id=scm.scm_id and t.seat_id=s.seat_id
            and t.sc_id= s.sc_id and scm.movie_id = m.movie_id and u.u_id='{user_id}';"""
        st.write("User's tikcets")
        try:
            t_counts = query_db(sql_ticket).loc[0].iat[2]
            username= query_db(sql_ticket).loc[0].iat[1]
            ticket_info=query_db(sql_ticket_u)
            t_counts = int(t_counts)
            if t_counts != 0:
                st.info(f"{username} has {t_counts} tickets reserved")
                st.code(ticket_info)
                ticket_prices=query_db(sql_ticket_u)["price"].tolist()
                sum=sum(ticket_prices)
                st.subheader(f"The total price {sum}")
        except:
            st.warning("Sorry! user has not booked any ticket.")
            
   