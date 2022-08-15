import mysql.connector
import pandas as pd

cn = mysql.connector.connect(user='root', password='12342234',
                                      host='127.0.0.1',
                                      database='dyscalculia')

cursor = cn.cursor(buffered=True)

cursor.execute(("SELECT * FROM trial_result_new;"))
rows = cursor.fetchall()

cn.commit()
cn.close()

headers = [i[0] for i in cursor.description]

df = pd.DataFrame(rows)

df.columns = headers

df.to_csv("trials_data.csv", index=False)