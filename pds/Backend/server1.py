#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import json
import pickle
import os.path
from os import path
import shutil
import subprocess
import pymongo
import uuid
import pandas as pd
from pulp import *
import excelrd
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import time
import secrets
import string
from datetime import datetime

app = Flask(__name__)
CORS(app)

#CORS(app, resources={r"/": {"origins": ""}})

UPLOAD_FOLDER = 'Backend'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def count_distinct_months(input_str):
    months_list = [month.strip() for month in input_str.split(',')]
    unique_months_count = len(set(months_list))
    return unique_months_count

def generate_random_id(length=14):
    alphabet = string.ascii_letters + string.digits
    random_id = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_id


def connect_to_database():
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'pds'
    connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    return connection


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hi, PDS!'


@app.route('/get_users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        connection = connect_to_database()
        user_list = []

        if connection.is_connected():
            cursor = connection.cursor()
            query = 'SELECT * FROM login WHERE 1'
            cursor.execute(query)
            user = cursor.fetchall()
            connection.close()

            if user:
                for row in user:
                    temp = {'username': row[0], 'password': row[1], '_id': row[2]}
                    user_list.append(temp)
                return jsonify(user_list)
            else:
                return jsonify(user_list)
        else:
            return jsonify(user_list)

@app.route('/extract_db', methods=['POST'])
def extract_db():
    if request.method == 'POST':
        connection = connect_to_database()
        warehouse_data = []
        fps_data = []
        all_data = {}
        applicableCount = request.form.get('applicable')

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM warehouse WHERE active='1'"
            cursor.execute(query)
            user = cursor.fetchall()
            
            if user:
                for row in user:
                    temp = {'State Name':'','WH_District': row[0], 'WH_Name': row[1], 'WH_ID': row[2], 'Type of WH': row[3], 'WH_Lat': row[5], 'WH_Long': row[6], 'Storage_Capacity': row[7], 'Owned/Rented':'', 'Quantity of Wheat stored (Quintals)':''}
                    warehouse_data.append(temp)
                    
            cursor = connection.cursor()
            query = "SELECT * FROM fps WHERE active='1'"
            cursor.execute(query)
            user = cursor.fetchall()
            connection.close()

            if user:
                for row in user:
                    temp = {'State Name':'','FPS_District': row[0], 'FPS_Name': row[1], 'FPS_ID': row[2], 'Motorable/Non-Motorable': row[3], 'FPS_Lat': row[6], 'FPS_Long': row[5], 'Allocation_Wheat': float(row[4])*int(applicableCount), 'FPS_Tehsil':''}
                    fps_data.append(temp)
                
            all_data["warehouse"] = warehouse_data
            all_data["fps"] = fps_data
            json_file_path = 'output.json'
            with open(json_file_path, 'w') as json_file:
                json.dump(all_data, json_file, indent=2)
        else:
            json_file_path = 'output.json'
            with open(json_file_path, 'w') as json_file:
                json.dump(all_data, json_file, indent=2)
        
        json_file_path = 'output.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        wh = pd.DataFrame(data['warehouse'])
        fps = pd.DataFrame(data['fps'])
        wh = wh.loc[:,["State Name","WH_District",'WH_Name',"WH_ID","Type of WH",'WH_Lat',"WH_Long","Storage_Capacity","Owned/Rented","Quantity of Wheat stored (Quintals)"]]
        fps = fps.loc[:,["State Name","FPS_District",'FPS_Name',"FPS_ID","Motorable/Non-Motorable",'FPS_Lat',"FPS_Long","Allocation_Wheat","FPS_Tehsil"]]

        # Rename the columns to make them valid Python identifiers
        column_mapping = {
            'Type of WH': 'Type of WH ( SWC, CWC, FCI, CAP, other)',
            'Storage_Capacity': 'Storage_Capacity',
            'WH_District': 'WH_District',
            'WH_ID': 'WH_ID',
            'WH_Lat': 'WH_Lat',
            'WH_Long': 'WH_Long',
            'WH_Name': 'WH_Name'
        }

        wh.rename(columns=column_mapping, inplace=True)

        # Save DataFrames to Excel file
        with pd.ExcelWriter('Backend//Data_1.xlsx') as writer:
            wh.to_excel(writer, sheet_name='A.1 Warehouse', index=False)
            fps.to_excel(writer, sheet_name='A.2 FPS', index=False)

        return {"success":1}
    
@app.route('/uploadConfigExcel', methods=['POST'])
def upload_config_excel():
    data = {}
    try:
        file = request.files['uploadFile']
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Data_1.xlsx')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)
            data['status'] = 1
            df = pd.read_excel(file_path)
        else:
            data['status'] = 0
            data['message'] = 'Invalid file. Only .xlsx or .xls files are allowed.'
    except Exception as e:
        data['status'] = 0
        data['message'] = 'Error uploading file'
        
        
    input = pd.ExcelFile('Backend//Data_1.xlsx')
    node1 = pd.read_excel(input,sheet_name="A.1 Warehouse")
    node2 = pd.read_excel(input,sheet_name="A.2 FPS")
    dist = [[0 for a in range(len(node2["FPS_ID"]))] for b in range(len(node1["WH_ID"]))]
    phi_1 = []
    phi_2 = []
    delta_phi = []
    delta_lambda = []
    R = 6371 

    for i in node1.index:
        for j in node2.index:
            phi_1=math.radians(node1["WH_Lat"][i])
            phi_2=math.radians(node2["FPS_Lat"][j])
            delta_phi=math.radians(node2["FPS_Lat"][j]-node1["WH_Lat"][i])
            delta_lambda=math.radians(node2["FPS_Long"][j]-node1["WH_Long"][i])
            x=math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
            y=2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))
            dist[i][j]=R*y
            
    dist=np.transpose(dist)
    df3 = pd.DataFrame(data = dist, index = node2['FPS_ID'], columns = node1['WH_ID'])
    df3.to_excel('Backend//Distance_Matrix.xlsx', index=True)
    return jsonify(data)



@app.route('/getfcidata', methods=['POST'])
def fci_data():
    try:
        usn = pd.ExcelFile('Backend//Data_1.xlsx')
        fci = pd.read_excel(usn, sheet_name='A.1 Warehouse', index_col=None)
        fps = pd.read_excel(usn, sheet_name='A.2 FPS', index_col=None)
       
        warehouse_no = fci['WH_ID'].nunique()
        fps_no = fps['FPS_ID'].nunique()
        combined_districts = pd.concat([fci['WH_District'],fps['FPS_District']])
        districts_no = combined_districts.nunique()
        total_demand = int(fps['Allocation_Wheat'].sum())
        total_supply = int(fci['Storage_Capacity'].sum())

        result = {'Warehouse_No': warehouse_no, 'FPS_No': fps_no, 'Total_Demand': total_demand, 'Total_Supply': total_supply, 'District_Count': districts_no}
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)})


@app.route('/getGraphData', methods=['POST'])
def graph_data():
    try:
        usn = pd.ExcelFile('Backend//Data_1.xlsx')
        FCI = pd.read_excel(usn, sheet_name='A.1 Warehouse', index_col=None)
        FPS = pd.read_excel(usn, sheet_name='A.2 FPS', index_col=None)

        
        District_Capacity = {}
        for i in range(len(FCI["WH_District"])):
            District_Name = FCI["WH_District"][i]
            if District_Name not in District_Capacity:
                District_Capacity[District_Name] = int(FCI["Storage_Capacity"][i])
            else:
                District_Capacity[District_Name] += int(FCI["Storage_Capacity"][i])
                
        District_Demand = {}
        for i in range(len(FPS["FPS_District"])):
            District_Name_FPS = FPS["FPS_District"][i]
            if District_Name_FPS not in District_Demand:
                District_Demand[District_Name_FPS] = int(FPS["Allocation_Wheat"][i])
            else:
                District_Demand[District_Name_FPS] += int(FPS["Allocation_Wheat"][i])
                
        District_Name = []
        District_Name2=[]
        District_Name = [i for i in District_Demand if i not in District_Capacity]
        District_Name2 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] >= District_Capacity[i]]
        District_Name_1 = {}
        District_Name_1['District_Name_All'] = District_Name + District_Name2
        District_Name3 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] <= District_Capacity[i]]


        
        combined_data = {'District_Demand': District_Demand, 'District_Capacity': District_Capacity, 'District_Name': District_Name_1}
        #print(District_Demand)
        #print(District_Capacity)
        print(District_Name_1)
        
        return jsonify(combined_data)
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)})


def check_id_exists(connection, random_id):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM optimised_table WHERE id = %s"
    cursor.execute(query, (random_id,))
    connection.commit()
    result = cursor.fetchone()[0]
    return result > 0

def check_year_month_exists(connection, month, year):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM optimised_table WHERE month = %s and year = %s"
    cursor.execute(query, (month,year,))
    connection.commit()
    result = cursor.fetchone()[0]
    return result > 0

def get_year_month_exists(connection, month, year):
    cursor = connection.cursor()
    query = "SELECT id FROM optimised_table WHERE month = %s and year = %s"
    cursor.execute(query, (month,year,))
    connection.commit()
    result = cursor.fetchone()
    return result[0] if result else None

#@app.route('/saveToDatabase', methods=['GET'])
def save_to_database(month, year, applicable):
    connection = connect_to_database()
    random_id = generate_random_id()
    while (check_id_exists(connection,random_id)):
        random_id = generate_random_id()
    table_name = "optimiseddata_" + str(random_id)
    warehouse_table = "warehouse_" + str(random_id)
    fps_table = "fps_" + str(random_id)
    if connection.is_connected():
        cursor = connection.cursor()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if(check_year_month_exists(connection, month, year)):
            existingid = get_year_month_exists(connection, month, year);
            sql = "UPDATE optimised_table set applicable='" + applicable + "', last_updated='" + formatted_datetime + "' WHERE id='" + existingid + "'"; 
            table_name = "optimiseddata_" + str(existingid)
            warehouse_table = "warehouse_" + str(existingid)
            fps_table = "fps_" + str(existingid)
            cursor.execute(sql)
        else:
            sql = "INSERT INTO optimised_table (id, month, year, applicable,last_updated) VALUES ('" + random_id + "','" + month + "','" + year + "','" + applicable + "','" + formatted_datetime + "')";
            cursor.execute(sql)
        
        connection.commit()
        warehouse_drop_query = 'DROP TABLE IF EXISTS ' + warehouse_table;
        cursor.execute(warehouse_drop_query)
        connection.commit()
        create_warehouse_query = ("CREATE TABLE " + warehouse_table + " (district VARCHAR(100) NOT NULL, name VARCHAR(100) NOT NULL, id VARCHAR(100) NOT NULL, warehousetype VARCHAR(100) NOT NULL, type VARCHAR(100) NOT NULL, latitude VARCHAR(100) NOT NULL, longitude VARCHAR(100) NOT NULL, storage VARCHAR(100) NOT NULL, uniqueid VARCHAR(100) NOT NULL, active VARCHAR(10) NOT NULL DEFAULT '1')")
        cursor.execute(create_warehouse_query)
        connection.commit()
        copy_warehouse_data = ("INSERT INTO " + warehouse_table + " SELECT * FROM warehouse WHERE active='1'")
        cursor.execute(copy_warehouse_data)
        connection.commit()
        
        fps_drop_query = 'DROP TABLE IF EXISTS ' + fps_table;
        cursor.execute(fps_drop_query)
        create_fps_query = ("CREATE TABLE " + fps_table + " (district VARCHAR(100) NOT NULL, name VARCHAR(100) NOT NULL, id VARCHAR(100) NOT NULL, type VARCHAR(100) NOT NULL, demand VARCHAR(100) NOT NULL, longitude VARCHAR(100) NOT NULL, latitude VARCHAR(100) NOT NULL, uniqueid VARCHAR(100) NOT NULL, active VARCHAR(10) NOT NULL DEFAULT '1')")
        cursor.execute(create_fps_query)
        connection.commit()
        copy_fps_data = ("INSERT INTO " + fps_table + " SELECT * FROM fps WHERE active='1'")
        cursor.execute(copy_fps_data)
        connection.commit()
        
        excel_file_path = 'Backend//Result_Sheet.xlsx'
        columns_to_fetch = ['Scenario','From','From_State','From_ID','From_Name','From_District','From_Lat','From_Long','To','To_State','To_ID','To_Name', 'To_District', 'To_Lat', 'To_Long','Commodity','Quantity','Distance']
        df = pd.read_excel(excel_file_path)
        selected_data = df[columns_to_fetch]
        sql = 'DROP TABLE IF EXISTS ' + table_name;
        cursor.execute(sql)
        connection.commit()
        
        sql = "CREATE TABLE " + table_name + " ( scenario VARCHAR(150) NOT NULL, `from` VARCHAR(150) NOT NULL,from_state VARCHAR(150) NOT NULL, from_id VARCHAR(150) NOT NULL, from_name VARCHAR(150) NOT NULL, from_district VARCHAR(150) NOT NULL, from_lat VARCHAR(150) NOT NULL,from_long VARCHAR(150) NOT NULL, `to` VARCHAR(150) NOT NULL,to_state VARCHAR(150) NOT NULL,to_id VARCHAR(150) NOT NULL, to_name VARCHAR(150) NOT NULL, to_district VARCHAR(150) NOT NULL, to_lat VARCHAR(150) NOT NULL, to_long VARCHAR(150) NOT NULL, commodity VARCHAR(150) NOT NULL,quantity VARCHAR(150) NOT NULL, distance VARCHAR(150) NOT NULL, approve VARCHAR(100) , new_id VARCHAR(100) , new_id_admin VARCHAR(100), old_id VARCHAR(100) , new_name VARCHAR(255) , reviewed VARCHAR(10) )";
        cursor.execute(sql)
        connection.commit()
        
        for (index, row) in selected_data.iterrows():
            sql = 'INSERT INTO ' + table_name + ' (`scenario`, `from`, `from_state`, `from_id`, `from_name`, `from_district`, `from_lat`, `from_long`, `to`, `to_state`, `to_id`, `to_name`, `to_district`, `to_lat`, `to_long`, `commodity`, `quantity`, `distance`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            values = tuple(row)
            cursor.execute(sql, values)
            connection.commit()
 
    if connection.is_connected():
        cursor.close()
        connection.close()
    return jsonify({'status': 1})

#@app.route('/saveMonthlyData', methods=['POST'])
def save_monthly_data(month, year, data):
    connection = connect_to_database()
    table_name = "optimised_table"
    
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Check if data for the given year and month already exists
            sql_check = "SELECT id FROM " + table_name + " WHERE year = %s AND month = %s"
            cursor.execute(sql_check, (year, month))
            existing_data = cursor.fetchone()

            if existing_data:
                # Update existing data
                sql_update = "UPDATE " + table_name + " SET data = %s WHERE id = %s"
                values_update = (data, existing_data[0])
                cursor.execute(sql_update, values_update)
            else:
                # Insert new data
                random_id = str(uuid.uuid4())
                sql_insert = "INSERT INTO " + table_name + " (month, year, data, id) VALUES (%s, %s, %s, %s)"
                values_insert = (month, year, data, random_id)
                cursor.execute(sql_insert, values_insert)
            connection.commit()
    except mysql.connector.Error as err:
        # Handle the error, print or log it
        print(f"Error: {err}")
        return jsonify({'status': 0, 'error': str(err)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return jsonify({'status': 1})



@app.route('/readMonthlyData', methods=['POST'])
def get_monthly_data():
    try:
        connection = connect_to_database()
        table_name = "optimised_table"

        if connection.is_connected():
            cursor = connection.cursor()

            # Retrieve all data from the monthlydata table
            sql_select_all = "SELECT year, month, data FROM " + table_name
            cursor.execute(sql_select_all)
            data_rows = cursor.fetchall()

            # Convert data to a list of dictionaries
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in data_rows]

    except mysql.connector.Error as err:
        # Handle the error, print or log it
        print(f"Error: {err}")
        return jsonify({'status': 0, 'error': str(err)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return jsonify({'status': 1, 'data': result})
   


@app.route('/processFile', methods=['POST'])
def processFile():
    scenario_type = request.form.get('type')
    if scenario_type == "intra":
        message = 'DataFile file is incorrect'
        try:
            USN = pd.ExcelFile('Backend//Data_1.xlsx')
            month = request.form.get('month')        
            year = request.form.get('year')
            applicable = request.form.get('applicable')
        except Exception as e:
            data = {}
            data['status'] = 0
            data['message'] = message
            json_data = json.dumps(data)
            json_object = json.loads(json_data)
            return json.dumps(json_object, indent=1)
        input = pd.ExcelFile('Backend//Data_1.xlsx')
        node1 = pd.read_excel(input,sheet_name="A.1 Warehouse")
        node2 = pd.read_excel(input,sheet_name="A.2 FPS")

        node1 = pd.read_excel(input,sheet_name="A.1 Warehouse")
        node2 = pd.read_excel(input,sheet_name="A.2 FPS")
        dist = [[0 for a in range(len(node2["FPS_ID"]))] for b in range(len(node1["WH_ID"]))]
        phi_1 = []
        phi_2 = []
        delta_phi = []
        delta_lambda = []
        R = 6371 

        for i in node1.index:
            for j in node2.index:
                phi_1=math.radians(node1["WH_Lat"][i])
                phi_2=math.radians(node2["FPS_Lat"][j])
                delta_phi=math.radians(node2["FPS_Lat"][j]-node1["WH_Lat"][i])
                delta_lambda=math.radians(node2["FPS_Long"][j]-node1["WH_Long"][i])
                x=math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
                y=2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))
                dist[i][j]=R*y
                
        dist=np.transpose(dist)
        df3 = pd.DataFrame(data = dist, index = node2['FPS_ID'], columns = node1['WH_ID'])
        df3.to_excel('Backend//Distance_Matrix.xlsx', index=True)

        WKB = excelrd.open_workbook('Backend//Distance_Matrix.xlsx')
        Sheet1 = WKB.sheet_by_index(0)
        FCI = pd.read_excel(USN, sheet_name='A.1 Warehouse', index_col=None)
        FPS = pd.read_excel(USN, sheet_name='A.2 FPS', index_col=None)

        FCI['WH_District'] = FCI['WH_District'].apply(lambda x: x.replace(' ', ''))
        FPS['FPS_District'] = FPS['FPS_District'].apply(lambda x: x.replace(' ', ''))

        Warehouse_No = []
        FPS_No = []
        Warehouse_No = FCI['WH_ID'].nunique()
        FPS_No = FPS['FPS_ID'].nunique()
        Warehouse_Count = {}

        FPS_Count = {}
        Warehouse_Count['Warehouse_Count'] = Warehouse_No
        FPS_Count['FPS_Count'] = FPS_No  # No of FPS

        Total_Supply = []
        Total_Supply_Warehouse = {}
        Total_Supply = FCI['Storage_Capacity'].sum()
        Total_Supply_Warehouse['Total_Supply_Warehouse'] = Total_Supply  # Total SUPPLY

        Total_Demand = []
        Total_Demand_FPS = {}
        Total_Demand = FPS['Allocation_Wheat'].sum()
        Total_Demand_FPS['Total_Demand_Warehouse'] = Total_Demand  # Total demand

        FCI_district = []
        FCI_Data = {}
        Disrticts_FCI = {}

        for (i, j) in zip(FCI['WH_District'], FCI['WH_ID']):
            i = i.lower()
            if i not in FCI_district:
                FCI_district.append(i)
                globals()['FCI_' + str(i)] = []
            globals()['FCI_' + str(i)].append(j)
        for i in FCI_district:
            FCI_Data[i] = globals()['FCI_' + str(i)]
        Disrticts_FCI['Disrticts_FCI'] = FCI_district

        District_Capacity = {}
        for i in range(len(FCI['WH_District'])):
            District_Name = FCI['WH_District'][i]
            if District_Name not in District_Capacity:
                District_Capacity[District_Name] = FCI['Storage_Capacity'][i]
            else:
                District_Capacity[District_Name] = FCI['Storage_Capacity'][i] + District_Capacity[District_Name]

        FPS_district = []
        FPS_Data = {}
        Districts_FPS = {}
        for (i, j) in zip(FPS['FPS_District'], FPS['FPS_Tehsil']):
            i = i.lower()
            if i not in FPS_district:
                FPS_district.append(i)
                globals()['FPS_' + str(i)] = []
            if j not in globals()['FPS_' + str(i)]:
                globals()['FPS_' + str(i)].append(j)
        for i in FPS_district:
            FPS_Data[i] = globals()['FPS_' + str(i)]
            Districts_FPS['Districts_FPS'] = FPS_district

        District_Demand = {}
        for i in range(len(FPS['FPS_District'])):
            District_Name_FPS = FPS['FPS_District'][i]
            if District_Name_FPS not in District_Demand:
                District_Demand[District_Name_FPS] = FPS['Allocation_Wheat'][i]
            else:
                District_Demand[District_Name_FPS] = FPS['Allocation_Wheat'][i] + District_Demand[District_Name_FPS]

        FCI_district = []
        FCI_Data = {}
        Disrticts_FCI = {}
        Data_state_wise = {}
        Data_statewise = {}

        for (i, j) in zip(FCI['WH_District'], FCI['WH_ID']):
            i = i.lower()
            if i not in FCI_district:
                FCI_district.append(i)
                globals()['FCI_' + str(i)] = []
            globals()['FCI_' + str(i)].append(j)
        for i in FCI_district:
            FCI_Data[i] = globals()['FCI_' + str(i)]
        Disrticts_FCI['Disrticts_FCI'] = FCI_district

        FPS_district = []
        FPS_Data = {}
        Districts_FPS = {}
        for (i, j) in zip(FPS['FPS_District'], FPS['FPS_Tehsil']):
            i = i.lower()
            if i not in FPS_district:
                FPS_district.append(i)
                globals()['FPS_' + str(i)] = []
            if j not in globals()['FPS_' + str(i)]:
                globals()['FPS_' + str(i)].append(j)
        for i in FPS_district:
            FPS_Data[i] = globals()['FPS_' + str(i)]
        Districts_FPS['Districts_FPS'] = FPS_district

        model = LpProblem('Supply-Demand-Problem', LpMinimize)

        Variable1 = []
        Variable2 = []
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                Variable1.append(str(FCI['WH_ID'][i]) + '_'
                                 + str(FCI['WH_District'][i]) + '_'
                                 + str(FPS['FPS_ID'][j]) + '_'
                                 + str(FPS['FPS_District'][j]) + '_Wheat')

        # Variables for Wheat from lEVEL2 TO FPS

        DV_Variables1 = LpVariable.matrix('X', Variable1, cat='float',
                lowBound=0)
        Allocation1 = np.array(DV_Variables1).reshape(len(FCI['WH_ID']),
                len(FPS['FPS_ID']))

        Variable1I = []
        Allocation1I = []
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                Variable1I.append(str(FCI['WH_ID'][i]) + '_'
                                  + str(FCI['WH_District'][i]) + '_'
                                  + str(FPS['FPS_ID'][j]) + '_'
                                  + str(FPS['FPS_District'][j]) + '_Wheat1')

    #    Variables for Wheat from IG TO FPS

        DV_Variables1I = LpVariable.matrix('X', Variable1I, cat='Binary',lowBound=0)
        Allocation1I = np.array(DV_Variables1I).reshape(len(FCI['WH_ID']),len(FPS['FPS_ID']))

        for i in range(len(FPS['FPS_ID'])):
             model += lpSum(Allocation1I[k][i] for k in range(len(FCI['WH_ID']))) <= 1

        for i in range(len(FCI['WH_ID'])):
             for j in range(len(FPS['FPS_ID'])):
                model += Allocation1[i][j] <= 1000000 * Allocation1I[i][j]
        
        District_Capacity = {}
        for i in range(len(FCI["WH_District"])):
            District_Name = FCI["WH_District"][i]
            if District_Name not in District_Capacity:
                District_Capacity[District_Name] = int(FCI["Storage_Capacity"][i])
            else:
                District_Capacity[District_Name] += int(FCI["Storage_Capacity"][i])
                
        District_Demand = {}
        for i in range(len(FPS["FPS_District"])):
            District_Name_FPS = FPS["FPS_District"][i]
            if District_Name_FPS not in District_Demand:
                District_Demand[District_Name_FPS] = int(FPS["Allocation_Wheat"][i])
            else:
                District_Demand[District_Name_FPS] += int(FPS["Allocation_Wheat"][i])
        District_Name = []
        District_Name2=[]
        District_Name = [i for i in District_Demand if i not in District_Capacity]
        District_Name4 = [i for i in District_Capacity if i not in District_Demand]
        District_Name2 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] >= District_Capacity[i]]
        District_Name_1 = {}
        District_Name_1['District_Name_All'] = District_Name + District_Name2
        District_Name3 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] <= District_Capacity[i]]
        
        
        name1 = []
        lst1 = []
        for j in range(len(DV_Variables1)):
            name1 = str(DV_Variables1[j])
            lst1 = name1.split("_")
            if lst1[2] in District_Name3 and lst1[4] in District_Name3 and lst1[2]!=lst1[4]:
                model+=DV_Variables1[j]==0
                #print(DV_Variables1[j]==0)
                
        name2 = []
        lst2 = []
        for j in range(len(DV_Variables1)):
            name2 = str(DV_Variables1[j])
            lst2 = name2.split("_")
            if lst2[2] in District_Name2 and lst2[4] in District_Name3:
                model+=DV_Variables1[j]==0
                #print(DV_Variables1[j]==0)
                
        name3 = []
        lst3 = []
        for j in range(len(DV_Variables1)):
            name3 = str(DV_Variables1[j])
            lst3 = name3.split("_")
            if lst3[2] in District_Name2 and lst3[4] in District_Name2 and lst3[2]!=lst3[4]:
                model+=DV_Variables1[j]==0
                #print(DV_Variables1[j]==0)

        name4 = []
        lst4 = []
        for j in range(len(DV_Variables1)):
            name4 = str(DV_Variables1[j])
            lst4 = name4.split("_")
            if lst4[2] in District_Name4 and lst4[4] in District_Name3:
                model+=DV_Variables1[j]==0
                #print(DV_Variables1[j]==0)

        Tehsil = {}
        UniqueId = 0
        Tehsil_temp = []
        Tehsil_rev = {}

        for i in FPS['FPS_Tehsil']:
            Tehsil_temp.append(i)
            if i not in Tehsil:
                Tehsil[i] = UniqueId
                Tehsil_rev[UniqueId] = i
                UniqueId = UniqueId + 1

        Tehsil_FPS = []
        for i in range(len(FPS['FPS_ID'])):
            Tehsil_FPS.append(Tehsil[Tehsil_temp[i]])

        PC_Mill = []
        for col in range(Sheet1.nrows):
            if col==0:
                continue
            temp = []
            for row in range (Sheet1.ncols):
                if row==0:
                    continue
                temp.append(Sheet1.cell_value(col,row))
            PC_Mill.append(temp)

        FCI_FPS = [[ PC_Mill[j][i] for j in range(len( PC_Mill))] for i in range(len( PC_Mill[0]))]

        allCombination1 = []

        for i in range(len(FCI_FPS)):
            for j in range(len(FPS['FPS_ID'])):
                allCombination1.append(Allocation1[i][j] * FCI_FPS[i][j])

        model += lpSum(allCombination1)

        # Demand Constraints for Wheat

        for i in range(len(FPS['FPS_ID'])):
            model += lpSum(Allocation1[j][i] for j in range(len(FCI['WH_ID'
                           ]))) >= FPS['Allocation_Wheat'][i]

        # Supply Constraints for Warehouses

        for i in range(len(FCI['WH_ID'])):
            model += lpSum(Allocation1[i][j] for j in range(len(FPS['FPS_ID'
                           ]))) <= FCI['Storage_Capacity'][i]

       # Calling CBC_CMB Solver

        #model.solve(CPLEX_CMD(options=['set mip tolerances mipgap 0.01']))
        #model.prob.solve(CPLEX_CMD(options=["set mip tolerances mipgap 0.03","set emphasis memory y"]))
        #model.solve(CPLEX_CMD(options=['set mip tolerances mipgap 0.03',"set emphasis memory y"]))
        model.solve(PULP_CBC_CMD())
        Status = LpStatus[model.status]

        Original_Cost = 100000000
        total = Original_Cost

        data = {}
        #data['status'] = 1
        #data['modelStatus'] = Status
        #data['totalCost'] = float(round(model.objective.value(),1))
        #data['original'] = float(round(total, 2))
        #data['percentageReduction'] = float(round((total
                #- model.objective.value()) / total, 4) * 100)
        #data['Average_Distance'] = float(round(model.objective.value(), 2)) / Total_Demand
        #data['Demand'] = int(FPS['Allocation_Wheat'].sum())

        BGW = {}
        BGR = {}
        IGW = {}
        IGR = {}
        FCIW = {}

        BGCapacity = {}

        temp = {}
        for i in range(len(FCI['WH_ID'])):
            temp[str(FCI['WH_ID'][i])] = str(FCI['Storage_Capacity'])
        BGCapacity = temp

        temp1 = {}
        BG_FPS = [[] for i in range(len(Tehsil))]
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                BG_FPS[Tehsil_FPS[j]].append(Allocation1[i][j].value())
            temp1[str(FCI['WH_ID'][i])] = \
                str(lpSum(Allocation1[i][j].value() for j in
                    range(len(FPS['FPS_ID']))))
            BGCapacity[str(FCI['WH_ID'][i])] = str(FCI['Storage_Capacity'
                    ][i])
        BGW['FPS'] = temp1

        BG_FPS_Wheat = {}
        for i in range(len(Tehsil)):
            BG_FPS_Wheat[str(Tehsil_rev[i])] = str(lpSum(BG_FPS[i]))

        BG_FPS_Rice = {}
        for i in range(len(Tehsil)):
            BG_FPS_Rice[str(Tehsil_rev[i])] = str(lpSum(BG_FPS[i]))

        data['BGW'] = BGW
        data['BGR'] = BGR
        data['FPSW'] = BG_FPS_Wheat
        data['FPSR'] = BG_FPS_Rice
        data['BGCapacity'] = BGCapacity

        wheat_total_dict = data['BGW']['FPS']

        wheat_total = 0
        for value in wheat_total_dict:
            if float(wheat_total_dict[value]):
                wheat_total = int(wheat_total + float(wheat_total_dict[value]))

        total_commodity = int(wheat_total)

        Output_File = open('Backend//Inter_District1.csv', 'w')
        for v in model.variables():
            if v.value() > 0:
                Output_File.write(v.name + '\t' + str(v.value()) + '\n')


        df9 = pd.read_csv('Backend//Inter_District1.csv',header=None)
        df9.columns = ['Tagging']
        df9[[
            'Var',
            'WH_ID',
            'W_D',
            'FPS_ID',
            'FPS_D',
            'Commodity_Value',
            ]] = df9[df9.columns[0]].str.split('_', n=6, expand=True)
        del df9[df9.columns[0]]
        df9[['Commodity', 'Values']] = df9['Commodity_Value'
                ].str.split('\\t', n=1, expand=True)
        del df9['Commodity_Value']
        df9 = df9.drop(np.where(df9['Commodity'] == 'Wheat1')[0])
        df9.to_excel('Backend//Tagging_Sheet_Pre.xlsx', sheet_name='BG_FPS')
        df31 = pd.read_excel('Backend//Tagging_Sheet_Pre.xlsx')
        df31['WH_ID'] = df31['WH_ID'].astype(str)  # Convert to object type, adjust as needed
        FCI['WH_ID'] = FCI['WH_ID'].astype(str) 

        df4 = pd.merge(df31, FCI, on='WH_ID', how='inner')
        #df4 = pd.merge(df31, FCI, on='WH_ID', how='inner')
        df4 = df4[[
            'WH_ID',
            'WH_Name',
            'WH_District',
            'WH_Lat',
            'WH_Long',
            'FPS_ID',
            'Values',
            ]]
        df4 = pd.merge(df4, FPS, on='FPS_ID', how='inner')
        df51 = df4[[
            'WH_ID',
            'WH_Name',
            'WH_District',
            'WH_Lat',
            'WH_Long',
            'FPS_ID',
            'FPS_Name',
            'FPS_District',
            'FPS_Lat',
            'FPS_Long',
            'Values',
            ]]
        df51.insert(0, 'Scenario', 'Optimized')
        df51.insert(1, 'From', 'Depot')
        df51.insert(2, 'From_State', 'Punjab')
        df51.insert(7, 'To', 'FPS')
        df51.insert(8, 'To_State', 'Punjab')
        df51.insert(9, 'Commodity', 'Wheat')
        df51.rename(columns={
            'WH_ID': 'From_ID',
            'WH_Name': 'From_Name',
            'WH_Lat': 'From_Lat',
            'WH_Long': 'From_Long',
            }, inplace=True)
        df51.rename(columns={
            'FPS_ID': 'To_ID',
            'FPS_Name': 'To_Name',
            'FPS_Lat': 'To_Lat',
            'FPS_Long': 'To_Long',
            'Values' :'Quantity'
            }, inplace=True)
        df51.rename(columns={'WH_District': 'From_District',
                   'FPS_District': 'To_District'}, inplace=True)
        df51 = df51.loc[:, [
            'Scenario',
            'From',
            'From_State',
            'From_District',
            'From_ID',
            'From_Name',
            'From_Lat',
            'From_Long',
            'To',
            'To_ID',
            'To_Name',
            'To_State',
            'To_District',
            'To_Lat',
            'To_Long',
            'Commodity',
            'Quantity',
            ]]
        df51['From_ID'] = pd.to_numeric(df51['From_ID'], errors='coerce')
        df51.to_excel('Backend//Tagging_Sheet_Pre11.xlsx', sheet_name='BG_FPS1')
        data1 = pd.ExcelFile("Backend//Tagging_Sheet_Pre11.xlsx")
        df5 = pd.read_excel(data1,sheet_name="BG_FPS1")

        Cost = pd.ExcelFile("Backend//Distance_Punjab_Haversine3.xlsx")
        BG_BG = pd.read_excel(Cost,sheet_name="BG_BG")
        
        Distance_BG_BG = {}
        column_list_BG_BG = list(BG_BG.columns)
        #print(column_list_BG_BG)
        row_list_BG_BG = list(BG_BG.iloc[:, 0])
        #print(row_list_BG_BG )  
        for ind in df5.index:
            from_code= df5['From_ID'][ind] 
            to_code = df5['To_ID'][ind]
            if to_code in row_list_BG_BG and from_code in column_list_BG_BG:
                index_i = row_list_BG_BG.index(to_code)
                index_j = column_list_BG_BG.index(from_code)
                key = str(to_code) + "_" + str(from_code)
                Distance_BG_BG[key]= BG_BG.iloc[index_i , index_j]
                print(Distance_BG_BG[key])
            
        #df5["Tagging"]=df5['To_ID']+ '_' + df5['From_ID']
        df5["Tagging"] = df5['To_ID'].astype(str) + '_' + df5['From_ID'].astype(str)
        df5['Distance'] = df5['Tagging'].map(Distance_BG_BG)
        df5 = df5.replace('',pd.NaT).fillna('shallu')
        d5=df5.loc[df5['Distance'] == "shallu"]
        df5.to_excel('Backend//Result_Sheet12.xlsx',
                         sheet_name='Warehouse_FPS')
        Result_Sheet1=pd.ExcelFile("Backend//Result_Sheet12.xlsx")
        df6= pd.read_excel(Result_Sheet1,sheet_name="Warehouse_FPS")
        df7=df6.loc[df6['Distance'] == "shallu"]
        source3 = df7['From_ID']  # FCI is the source and FPS is the destination
        destination3 = df7['To_ID']
        BingMapsKey = "Aijr1qUbtll5hbUwkxCyoDmnsa8T_9XLAKTjRO6w0bFIfWahw2fbgIrItxpv8SPV"  # Bing Map Key
        df7["Warehouse_lat_long"]= df7['From_Lat'].astype(str) + ',' + df7['From_Long'].astype(str)
        df7["FPS_lat_long"]= df7['To_Lat'].astype(str) + ',' + df7['To_Long'].astype(str)

        #df8=df7["From_ID","To_ID","Warehouse_lat_long","FPS_lat_long"]
        df8 = df7[['From_ID', 'To_ID', 'Warehouse_lat_long', 'FPS_lat_long']]
        source3 = df8['From_ID']
        destination3 = df8['To_ID']
        dist3 = [0 for _ in range(len(destination3))]  # Transport matrix for FCI_FPS
        BingMapsKey = "Aijr1qUbtll5hbUwkxCyoDmnsa8T_9XLAKTjRO6w0bFIfWahw2fbgIrItxpv8SPV"  # Bing Map Key

        dist3 = []  # Initialize an empty list for distances

        for index, row in df8.iterrows():
            origin = row["Warehouse_lat_long"]
            dest = row["FPS_lat_long"]
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    response = requests.get(
                        "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=" + origin + "&destinations=" + dest +
                        "&travelMode=driving&key=" + BingMapsKey)
                    resp = response.json()

                    # Append a new element to dist3 for the current index
                    dist3.append(resp['resourceSets'][0]['resources'][0]['results'][0]['travelDistance'])

                    # Display the output for each iteration
                    print(f"Origin: {origin}, Destination: {dest}, Distance: {dist3[-1]}")
                    break  # Successful response, exit the retry loop
                except (requests.ConnectionError, requests.Timeout):
                    retries += 1
                    print(f"Attempt {retries} failed. Retrying...")
                    time.sleep(1)  # Wait for 1 second before retrying

        print("Final distances:", dist3)

        df7["Distance"]=dist3
        df7.drop(['Warehouse_lat_long', 'FPS_lat_long'], axis=1)
        df9=df6.loc[df6['Distance'] != "shallu"]
        df9 = df9.loc[:, [
                'Scenario',
                'From',
                'From_State',
                'From_District',
                'From_ID',
                'From_Name',
                'From_Lat',
                'From_Long',
                'To',
                'To_ID',
                'To_Name',
                'To_State',
                'To_District',
                'To_Lat',
                'To_Long',
                'Commodity',
                'Quantity',
                 "Distance",]]
        df7 = df7.loc[:, [
                'Scenario',
                'From',
                'From_State',
                'From_District',
                'From_ID',
                'From_Name',
                'From_Lat',
                'From_Long',
                'To',
                'To_ID',
                'To_Name',
                'To_State',
                'To_District',
                'To_Lat',
                'To_Long',
                'Commodity',
                'Quantity',
               "Distance"]]
        
        print(df9.head())  # Print the first few rows
        #df10 = df9.append([df7], ignore_index=True)
        df10 = pd.concat([df9, df7], ignore_index=True)
        #df10 = df9.append([df7],ignore_index=True)
        result = (df10['Quantity'] * df10['Distance']).sum()
        print(result)


        df10.to_excel('Backend//Result_Sheet.xlsx',
                     sheet_name='Warehouse_FPS')
        
        data["Scenario"]="Intra"
        data["Scenario_Baseline"] = "Baseline"
        
        data["WH_Used"] = df5['From_ID'].nunique()
        data["WH_Used_Baseline"] = "272"
        
        data["FPS_Used"] = df5['To_ID'].nunique()
        data["FPS_Used_Baseline"] = "17,781"
        
        data['Demand'] = int(FPS['Allocation_Wheat'].sum())
        data['Demand_Baseline'] = int(FPS['Allocation_Wheat'].sum())
        
        data['Total_QKM'] = float(result)
        data['Total_QKM_Baseline'] = "9,15,29,852"
        
        data['Average_Distance'] = float(round(result, 2)) / Total_Demand
        data['Average_Distance_Baseline'] = "10.52"
                     
        save_to_database(month, year, applicable)
        save_monthly_data(month, year, float(result))
        
        file_open = open('plantuml_file.txt', 'w')
        file_open.write('scale 600 width\n')
        file_open.write('scale 400 height\n')
        file_open.write('skinparam sequenceMessageAlign center\n')
        file_open.write('skinparam sequenceArrowThickness 3\n')
        file_open.write('skinparam backgroundColor #FFFFFF\n')
        file_open.write('hide footbox\n')
        file_open.write('title <font color=#000000 size=20> Allocation Movement \n')
        file_open.write('skinparam sequence{\n')
        file_open.write('ParticipantBorderColor none\n')
        file_open.write('ParticipantBackgroundColor #004699\n')
        file_open.write('ParticipantFontName calibri\n')
        file_open.write('ParticipantFontSize 15\n')
        file_open.write('ParticipantFontColor #ffffff\n')
        file_open.write('}\n')
        file_open.write('participant "FCI\\n<size:40><&globe>" as FCI order  1 \n')
        file_open.write('participant "FPS\\n<size:40><&vertical-align-top>" as FPS order 2 \n')
        file_open.write('participant "FCI\\n<size:40><&globe>" as FCI order  1 \n')
        file_open.write('participant "FPS\\n<size:40><&vertical-align-top>" as FPS order 2 \n')
        file_open.write('FCI -[#32a8a0]> FPS: <font color=#0915ed> ' + str(total_commodity) + ' \n')
        file_open.write('hnote over FCI, FPS #ffffff: ' + str(wheat_total) + ',' + ' Qtl Wheat \n')
        file_open.close()
        command = 'python -m plantuml plantuml_file.txt'
        subprocess.run(command, shell=True)

        json_data = json.dumps(data)
        json_object = json.loads(json_data)

        if os.path.exists('ouputPickle.pkl'):
            os.remove('ouputPickle.pkl')

        # open pickle file
        dbfile1 = open('ouputPickle.pkl', 'ab')
        
    else:
        message = 'DataFile file is incorrect'
        try:
            USN = pd.ExcelFile('Backend//Data_1.xlsx')
            month = request.form.get('month')        
            year = request.form.get('year')
            scenario_type = request.form.get('type')
            applicable = request.form.get('applicable')
        except Exception as e:
            data = {}
            data['status'] = 0
            data['message'] = message
            json_data = json.dumps(data)
            json_object = json.loads(json_data)
            return json.dumps(json_object, indent=1)
        input = pd.ExcelFile('Backend//Data_1.xlsx')
        node1 = pd.read_excel(input,sheet_name="A.1 Warehouse")
        node2 = pd.read_excel(input,sheet_name="A.2 FPS")

        node1 = pd.read_excel(input,sheet_name="A.1 Warehouse")
        node2 = pd.read_excel(input,sheet_name="A.2 FPS")
        dist = [[0 for a in range(len(node2["FPS_ID"]))] for b in range(len(node1["WH_ID"]))]
        phi_1 = []
        phi_2 = []
        delta_phi = []
        delta_lambda = []
        R = 6371 

        for i in node1.index:
            for j in node2.index:
                phi_1=math.radians(node1["WH_Lat"][i])
                phi_2=math.radians(node2["FPS_Lat"][j])
                delta_phi=math.radians(node2["FPS_Lat"][j]-node1["WH_Lat"][i])
                delta_lambda=math.radians(node2["FPS_Long"][j]-node1["WH_Long"][i])
                x=math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
                y=2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))
                dist[i][j]=R*y
                
        dist=np.transpose(dist)
        df3 = pd.DataFrame(data = dist, index = node2['FPS_ID'], columns = node1['WH_ID'])
        df3.to_excel('Backend//Distance_Matrix.xlsx', index=True)

        WKB = excelrd.open_workbook('Backend//Distance_Matrix.xlsx')
        Sheet1 = WKB.sheet_by_index(0)
        FCI = pd.read_excel(USN, sheet_name='A.1 Warehouse', index_col=None)
        FPS = pd.read_excel(USN, sheet_name='A.2 FPS', index_col=None)

        FCI['WH_District'] = FCI['WH_District'].apply(lambda x: x.replace(' ', ''))
        FPS['FPS_District'] = FPS['FPS_District'].apply(lambda x: x.replace(' ', ''))

        Warehouse_No = []
        FPS_No = []
        Warehouse_No = FCI['WH_ID'].nunique()
        FPS_No = FPS['FPS_ID'].nunique()
        Warehouse_Count = {}

        FPS_Count = {}
        Warehouse_Count['Warehouse_Count'] = Warehouse_No
        FPS_Count['FPS_Count'] = FPS_No  # No of FPS

        Total_Supply = []
        Total_Supply_Warehouse = {}
        Total_Supply = FCI['Storage_Capacity'].sum()
        Total_Supply_Warehouse['Total_Supply_Warehouse'] = Total_Supply  # Total SUPPLY

        Total_Demand = []
        Total_Demand_FPS = {}
        Total_Demand = FPS['Allocation_Wheat'].sum()
        Total_Demand_FPS['Total_Demand_Warehouse'] = Total_Demand  # Total demand

        FCI_district = []
        FCI_Data = {}
        Disrticts_FCI = {}

        for (i, j) in zip(FCI['WH_District'], FCI['WH_ID']):
            i = i.lower()
            if i not in FCI_district:
                FCI_district.append(i)
                globals()['FCI_' + str(i)] = []
            globals()['FCI_' + str(i)].append(j)
        for i in FCI_district:
            FCI_Data[i] = globals()['FCI_' + str(i)]
        Disrticts_FCI['Disrticts_FCI'] = FCI_district

        District_Capacity = {}
        for i in range(len(FCI['WH_District'])):
            District_Name = FCI['WH_District'][i]
            if District_Name not in District_Capacity:
                District_Capacity[District_Name] = FCI['Storage_Capacity'][i]
            else:
                District_Capacity[District_Name] = FCI['Storage_Capacity'][i] + District_Capacity[District_Name]

        FPS_district = []
        FPS_Data = {}
        Districts_FPS = {}
        for (i, j) in zip(FPS['FPS_District'], FPS['FPS_Tehsil']):
            i = i.lower()
            if i not in FPS_district:
                FPS_district.append(i)
                globals()['FPS_' + str(i)] = []
            if j not in globals()['FPS_' + str(i)]:
                globals()['FPS_' + str(i)].append(j)
        for i in FPS_district:
            FPS_Data[i] = globals()['FPS_' + str(i)]
            Districts_FPS['Districts_FPS'] = FPS_district

        District_Demand = {}
        for i in range(len(FPS['FPS_District'])):
            District_Name_FPS = FPS['FPS_District'][i]
            if District_Name_FPS not in District_Demand:
                District_Demand[District_Name_FPS] = FPS['Allocation_Wheat'][i]
            else:
                District_Demand[District_Name_FPS] = FPS['Allocation_Wheat'][i] + District_Demand[District_Name_FPS]

        FCI_district = []
        FCI_Data = {}
        Disrticts_FCI = {}
        Data_state_wise = {}
        Data_statewise = {}

        for (i, j) in zip(FCI['WH_District'], FCI['WH_ID']):
            i = i.lower()
            if i not in FCI_district:
                FCI_district.append(i)
                globals()['FCI_' + str(i)] = []
            globals()['FCI_' + str(i)].append(j)
        for i in FCI_district:
            FCI_Data[i] = globals()['FCI_' + str(i)]
        Disrticts_FCI['Disrticts_FCI'] = FCI_district

        FPS_district = []
        FPS_Data = {}
        Districts_FPS = {}
        for (i, j) in zip(FPS['FPS_District'], FPS['FPS_Tehsil']):
            i = i.lower()
            if i not in FPS_district:
                FPS_district.append(i)
                globals()['FPS_' + str(i)] = []
            if j not in globals()['FPS_' + str(i)]:
                globals()['FPS_' + str(i)].append(j)
        for i in FPS_district:
            FPS_Data[i] = globals()['FPS_' + str(i)]
        Districts_FPS['Districts_FPS'] = FPS_district

        model = LpProblem('Supply-Demand-Problem', LpMinimize)

        Variable1 = []
        Variable2 = []
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                Variable1.append(str(FCI['WH_ID'][i]) + '_'
                                 + str(FCI['WH_District'][i]) + '_'
                                 + str(FPS['FPS_ID'][j]) + '_'
                                 + str(FPS['FPS_District'][j]) + '_Wheat')

        # Variables for Wheat from lEVEL2 TO FPS

        DV_Variables1 = LpVariable.matrix('X', Variable1, cat='float',
                lowBound=0)
        Allocation1 = np.array(DV_Variables1).reshape(len(FCI['WH_ID']),
                len(FPS['FPS_ID']))

        Variable1I = []
        Allocation1I = []
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                Variable1I.append(str(FCI['WH_ID'][i]) + '_'
                                  + str(FCI['WH_District'][i]) + '_'
                                  + str(FPS['FPS_ID'][j]) + '_'
                                  + str(FPS['FPS_District'][j]) + '_Wheat1')

    #    Variables for Wheat from IG TO FPS

        DV_Variables1I = LpVariable.matrix('X', Variable1I, cat='Binary',lowBound=0)
        Allocation1I = np.array(DV_Variables1I).reshape(len(FCI['WH_ID']),len(FPS['FPS_ID']))

        for i in range(len(FPS['FPS_ID'])):
             model += lpSum(Allocation1I[k][i] for k in range(len(FCI['WH_ID']))) <= 1

        for i in range(len(FCI['WH_ID'])):
             for j in range(len(FPS['FPS_ID'])):
                model += Allocation1[i][j] <= 1000000 * Allocation1I[i][j]
        
        District_Capacity = {}
        for i in range(len(FCI["WH_District"])):
            District_Name = FCI["WH_District"][i]
            if District_Name not in District_Capacity:
                District_Capacity[District_Name] = int(FCI["Storage_Capacity"][i])
            else:
                District_Capacity[District_Name] += int(FCI["Storage_Capacity"][i])
                
        District_Demand = {}
        for i in range(len(FPS["FPS_District"])):
            District_Name_FPS = FPS["FPS_District"][i]
            if District_Name_FPS not in District_Demand:
                District_Demand[District_Name_FPS] = int(FPS["Allocation_Wheat"][i])
            else:
                District_Demand[District_Name_FPS] += int(FPS["Allocation_Wheat"][i])
        District_Name = []
        District_Name2=[]
        District_Name = [i for i in District_Demand if i not in District_Capacity]
        District_Name4 = [i for i in District_Capacity if i not in District_Demand]
        District_Name2 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] >= District_Capacity[i]]
        District_Name_1 = {}
        District_Name_1['District_Name_All'] = District_Name + District_Name2
        District_Name3 = [i for i in District_Demand if i in District_Capacity and District_Demand[i] <= District_Capacity[i]]
        
        Tehsil = {}
        UniqueId = 0
        Tehsil_temp = []
        Tehsil_rev = {}

        for i in FPS['FPS_Tehsil']:
            Tehsil_temp.append(i)
            if i not in Tehsil:
                Tehsil[i] = UniqueId
                Tehsil_rev[UniqueId] = i
                UniqueId = UniqueId + 1

        Tehsil_FPS = []
        for i in range(len(FPS['FPS_ID'])):
            Tehsil_FPS.append(Tehsil[Tehsil_temp[i]])

        PC_Mill = []
        for col in range(Sheet1.nrows):
            if col==0:
                continue
            temp = []
            for row in range (Sheet1.ncols):
                if row==0:
                    continue
                temp.append(Sheet1.cell_value(col,row))
            PC_Mill.append(temp)

        FCI_FPS = [[ PC_Mill[j][i] for j in range(len( PC_Mill))] for i in range(len( PC_Mill[0]))]

        allCombination1 = []

        for i in range(len(FCI_FPS)):
            for j in range(len(FPS['FPS_ID'])):
                allCombination1.append(Allocation1[i][j] * FCI_FPS[i][j])

        model += lpSum(allCombination1)

        # Demand Constraints for Wheat

        for i in range(len(FPS['FPS_ID'])):
            model += lpSum(Allocation1[j][i] for j in range(len(FCI['WH_ID'
                           ]))) >= FPS['Allocation_Wheat'][i]

        # Supply Constraints for Warehouses

        for i in range(len(FCI['WH_ID'])):
            model += lpSum(Allocation1[i][j] for j in range(len(FPS['FPS_ID'
                           ]))) <= FCI['Storage_Capacity'][i]

       # Calling CBC_CMB Solver

        #model.solve(CPLEX_CMD(options=['set mip tolerances mipgap 0.01']))
        #model.prob.solve(CPLEX_CMD(options=["set mip tolerances mipgap 0.03","set emphasis memory y"]))
        #model.solve(CPLEX_CMD(options=['set mip tolerances mipgap 0.03',"set emphasis memory y"]))
        model.solve(PULP_CBC_CMD())
        Status = LpStatus[model.status]

        Original_Cost = 100000000
        total = Original_Cost

        data = {}
        #data['status'] = 1
        #data['modelStatus'] = Status
        #data['totalCost'] = float(round(model.objective.value(),1))
        #data['original'] = float(round(total, 2))
        #data['percentageReduction'] = float(round((total
                #- model.objective.value()) / total, 4) * 100)
        #data['Average_Distance'] = float(round(model.objective.value(), 2)) / Total_Demand
        #data['Demand'] = int(FPS['Allocation_Wheat'].sum())

        BGW = {}
        BGR = {}
        IGW = {}
        IGR = {}
        FCIW = {}

        BGCapacity = {}

        temp = {}
        for i in range(len(FCI['WH_ID'])):
            temp[str(FCI['WH_ID'][i])] = str(FCI['Storage_Capacity'])
        BGCapacity = temp

        temp1 = {}
        BG_FPS = [[] for i in range(len(Tehsil))]
        for i in range(len(FCI['WH_ID'])):
            for j in range(len(FPS['FPS_ID'])):
                BG_FPS[Tehsil_FPS[j]].append(Allocation1[i][j].value())
            temp1[str(FCI['WH_ID'][i])] = \
                str(lpSum(Allocation1[i][j].value() for j in
                    range(len(FPS['FPS_ID']))))
            BGCapacity[str(FCI['WH_ID'][i])] = str(FCI['Storage_Capacity'
                    ][i])
        BGW['FPS'] = temp1

        BG_FPS_Wheat = {}
        for i in range(len(Tehsil)):
            BG_FPS_Wheat[str(Tehsil_rev[i])] = str(lpSum(BG_FPS[i]))

        BG_FPS_Rice = {}
        for i in range(len(Tehsil)):
            BG_FPS_Rice[str(Tehsil_rev[i])] = str(lpSum(BG_FPS[i]))

        data['BGW'] = BGW
        data['BGR'] = BGR
        data['FPSW'] = BG_FPS_Wheat
        data['FPSR'] = BG_FPS_Rice
        data['BGCapacity'] = BGCapacity

        wheat_total_dict = data['BGW']['FPS']

        wheat_total = 0
        for value in wheat_total_dict:
            if float(wheat_total_dict[value]):
                wheat_total = int(wheat_total + float(wheat_total_dict[value]))

        total_commodity = int(wheat_total)

        Output_File = open('Backend//Inter_District1.csv', 'w')
        for v in model.variables():
            if v.value() > 0:
                Output_File.write(v.name + '\t' + str(v.value()) + '\n')

        Output_File = open('Backend//Inter_District1.csv', 'w')
        for v in model.variables():
            if v.value() > 0:
                Output_File.write(v.name + '\t' + str(v.value()) + '\n')

        df9 = pd.read_csv('Backend//Inter_District1.csv',header=None)
        
        df9.columns = ['Tagging']
        df9[[
            'Var',
            'WH_ID',
            'W_D',
            'FPS_ID',
            'FPS_D',
            'Commodity_Value',
            ]] = df9[df9.columns[0]].str.split('_', n=6, expand=True)
        del df9[df9.columns[0]]
        df9[['Commodity', 'Values']] = df9['Commodity_Value'
                ].str.split('\\t', n=1, expand=True)
        del df9['Commodity_Value']
        df9 = df9.drop(np.where(df9['Commodity'] == 'Wheat1')[0])
        df9.to_excel('Backend//Tagging_Sheet_Pre.xlsx', sheet_name='BG_FPS')
        df31 = pd.read_excel('Backend//Tagging_Sheet_Pre.xlsx')
        df31['WH_ID'] = df31['WH_ID'].astype(str)  # Convert to object type, adjust as needed
        FCI['WH_ID'] = FCI['WH_ID'].astype(str) 

        df4 = pd.merge(df31, FCI, on='WH_ID', how='inner')
        #df4 = pd.merge(df31, FCI, on='WH_ID', how='inner')
        df4 = df4[[
            'WH_ID',
            'WH_Name',
            'WH_District',
            'WH_Lat',
            'WH_Long',
            'FPS_ID',
            'Values',
            ]]
        df4 = pd.merge(df4, FPS, on='FPS_ID', how='inner')
        df51 = df4[[
            'WH_ID',
            'WH_Name',
            'WH_District',
            'WH_Lat',
            'WH_Long',
            'FPS_ID',
            'FPS_Name',
            'FPS_District',
            'FPS_Lat',
            'FPS_Long',
            'Values',
            ]]
        df51.insert(0, 'Scenario', 'Optimized')
        df51.insert(1, 'From', 'Depot')
        df51.insert(2, 'From_State', 'Punjab')
        df51.insert(7, 'To', 'FPS')
        df51.insert(8, 'To_State', 'Punjab')
        df51.insert(9, 'Commodity', 'Wheat')
        df51.rename(columns={
            'WH_ID': 'From_ID',
            'WH_Name': 'From_Name',
            'WH_Lat': 'From_Lat',
            'WH_Long': 'From_Long',
            }, inplace=True)
        df51.rename(columns={
            'FPS_ID': 'To_ID',
            'FPS_Name': 'To_Name',
            'FPS_Lat': 'To_Lat',
            'FPS_Long': 'To_Long',
            'Values':'Quantity',
            }, inplace=True)
        df51.rename(columns={'WH_District': 'From_District',
                   'FPS_District': 'To_District'}, inplace=True)
        df51 = df51.loc[:, [
            'Scenario',
            'From',
            'From_State',
            'From_District',
            'From_ID',
            'From_Name',
            'From_Lat',
            'From_Long',
            'To',
            'To_ID',
            'To_Name',
            'To_State',
            'To_District',
            'To_Lat',
            'To_Long',
            'Commodity',
            'Quantity',
            ]]
        df51['From_ID'] = pd.to_numeric(df51['From_ID'], errors='coerce')
        df51.to_excel('Backend//Tagging_Sheet_Pre11.xlsx', sheet_name='BG_FPS1')
        data1 = pd.ExcelFile("Backend//Tagging_Sheet_Pre11.xlsx")
        df5 = pd.read_excel(data1,sheet_name="BG_FPS1")

        Cost = pd.ExcelFile("Backend//Distance_Punjab_Haversine3.xlsx")
        BG_BG = pd.read_excel(Cost,sheet_name="BG_BG")
        
        Distance_BG_BG = {}
        column_list_BG_BG = list(BG_BG.columns)
        #print(column_list_BG_BG)
        row_list_BG_BG = list(BG_BG.iloc[:, 0])
        #print(row_list_BG_BG )  
        for ind in df5.index:
            from_code= df5['From_ID'][ind] 
            to_code = df5['To_ID'][ind]
            if to_code in row_list_BG_BG and from_code in column_list_BG_BG:
                index_i = row_list_BG_BG.index(to_code)
                index_j = column_list_BG_BG.index(from_code)
                key = str(to_code) + "_" + str(from_code)
                Distance_BG_BG[key]= BG_BG.iloc[index_i , index_j]
                print(Distance_BG_BG[key])
            
        #df5["Tagging"]=df5['To_ID']+ '_' + df5['From_ID']
        df5["Tagging"] = df5['To_ID'].astype(str) + '_' + df5['From_ID'].astype(str)
        df5['Distance'] = df5['Tagging'].map(Distance_BG_BG)
        df5 = df5.replace('',pd.NaT).fillna('shallu')
        d5=df5.loc[df5['Distance'] == "shallu"]
        df5.to_excel('Backend//Result_Sheet12.xlsx',
                         sheet_name='Warehouse_FPS')
        Result_Sheet1=pd.ExcelFile("Backend//Result_Sheet12.xlsx")
        df6= pd.read_excel(Result_Sheet1,sheet_name="Warehouse_FPS")
        df7=df6.loc[df6['Distance'] == "shallu"]
        source3 = df7['From_ID']  # FCI is the source and FPS is the destination
        destination3 = df7['To_ID']
        BingMapsKey = "Aijr1qUbtll5hbUwkxCyoDmnsa8T_9XLAKTjRO6w0bFIfWahw2fbgIrItxpv8SPV"  # Bing Map Key
        df7["Warehouse_lat_long"]= df7['From_Lat'].astype(str) + ',' + df7['From_Long'].astype(str)
        df7["FPS_lat_long"]= df7['To_Lat'].astype(str) + ',' + df7['To_Long'].astype(str)

        #df8=df7["From_ID","To_ID","Warehouse_lat_long","FPS_lat_long"]
        df8 = df7[['From_ID', 'To_ID', 'Warehouse_lat_long', 'FPS_lat_long']]
        source3 = df8['From_ID']
        destination3 = df8['To_ID']
        dist3 = [0 for _ in range(len(destination3))]  # Transport matrix for FCI_FPS
        BingMapsKey = "Aijr1qUbtll5hbUwkxCyoDmnsa8T_9XLAKTjRO6w0bFIfWahw2fbgIrItxpv8SPV"  # Bing Map Key

        dist3 = []  # Initialize an empty list for distances

        for index, row in df8.iterrows():
            origin = row["Warehouse_lat_long"]
            dest = row["FPS_lat_long"]
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    response = requests.get(
                        "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=" + origin + "&destinations=" + dest +
                        "&travelMode=driving&key=" + BingMapsKey)
                    resp = response.json()

                    # Append a new element to dist3 for the current index
                    dist3.append(resp['resourceSets'][0]['resources'][0]['results'][0]['travelDistance'])

                    # Display the output for each iteration
                    print(f"Origin: {origin}, Destination: {dest}, Distance: {dist3[-1]}")
                    break  # Successful response, exit the retry loop
                except (requests.ConnectionError, requests.Timeout):
                    retries += 1
                    print(f"Attempt {retries} failed. Retrying...")
                    time.sleep(1)  # Wait for 1 second before retrying

        print("Final distances:", dist3)

        df7["Distance"]=dist3
        df7.drop(['Warehouse_lat_long', 'FPS_lat_long'], axis=1)
        df9=df6.loc[df6['Distance'] != "shallu"]
        df9 = df9.loc[:, [
                'Scenario',
                'From',
                'From_State',
                'From_District',
                'From_ID',
                'From_Name',
                'From_Lat',
                'From_Long',
                'To',
                'To_ID',
                'To_Name',
                'To_State',
                'To_District',
                'To_Lat',
                'To_Long',
                'Commodity',
                'Quantity',
                 "Distance",]]
        df7 = df7.loc[:, [
                'Scenario',
                'From',
                'From_State',
                'From_District',
                'From_ID',
                'From_Name',
                'From_Lat',
                'From_Long',
                'To',
                'To_ID',
                'To_Name',
                'To_State',
                'To_District',
                'To_Lat',
                'To_Long',
                'Commodity',
                'Quantity',
               "Distance"]]
        
        print(df9.head())  # Print the first few rows
        #df10 = df9.append([df7], ignore_index=True)
        df10 = pd.concat([df9, df7], ignore_index=True)
        #df10 = df9.append([df7],ignore_index=True)
        result = (df10['Quantity'] * df10['Distance']).sum()
        print(result)


        df10.to_excel('Backend//Result_Sheet.xlsx',
                     sheet_name='Warehouse_FPS')
        
        data["Scenario"]="Inter"
        data["Scenario_Baseline"] = "Baseline"
        
        data["WH_Used"] = df5['From_ID'].nunique()
        data["WH_Used_Baseline"] = "272"
        
        data["FPS_Used"] = df5['To_ID'].nunique()
        data["FPS_Used_Baseline"] = "17,781"
        
        data['Demand'] = int(FPS['Allocation_Wheat'].sum())
        data['Demand_Baseline'] = int(FPS['Allocation_Wheat'].sum())
        
        data['Total_QKM'] = float(result)
        data['Total_QKM_Baseline'] = "9,15,29,852"
        
        data['Average_Distance'] = float(round(result, 2)) / Total_Demand
        data['Average_Distance_Baseline'] = "10.52"
                     
        save_to_database(month, year, applicable)
        save_monthly_data(month, year, float(result))
        
        file_open = open('plantuml_file.txt', 'w')
        file_open.write('scale 600 width\n')
        file_open.write('scale 400 height\n')
        file_open.write('skinparam sequenceMessageAlign center\n')
        file_open.write('skinparam sequenceArrowThickness 3\n')
        file_open.write('skinparam backgroundColor #FFFFFF\n')
        file_open.write('hide footbox\n')
        file_open.write('title <font color=#000000 size=20> Allocation Movement \n')
        file_open.write('skinparam sequence{\n')
        file_open.write('ParticipantBorderColor none\n')
        file_open.write('ParticipantBackgroundColor #004699\n')
        file_open.write('ParticipantFontName calibri\n')
        file_open.write('ParticipantFontSize 15\n')
        file_open.write('ParticipantFontColor #ffffff\n')
        file_open.write('}\n')
        file_open.write('participant "FCI\\n<size:40><&globe>" as FCI order  1 \n')
        file_open.write('participant "FPS\\n<size:40><&vertical-align-top>" as FPS order 2 \n')
        file_open.write('participant "FCI\\n<size:40><&globe>" as FCI order  1 \n')
        file_open.write('participant "FPS\\n<size:40><&vertical-align-top>" as FPS order 2 \n')
        file_open.write('FCI -[#32a8a0]> FPS: <font color=#0915ed> ' + str(total_commodity) + ' \n')
        file_open.write('hnote over FCI, FPS #ffffff: ' + str(wheat_total) + ',' + ' Qtl Wheat \n')
        file_open.close()
        command = 'python -m plantuml plantuml_file.txt'
        subprocess.run(command, shell=True)

        json_data = json.dumps(data)
        json_object = json.loads(json_data)

        if os.path.exists('ouputPickle.pkl'):
            os.remove('ouputPickle.pkl')

        # open pickle file
        dbfile1 = open('ouputPickle.pkl', 'ab')

    # save pickle data
    pickle.dump(json_object, dbfile1)
    dbfile1.close()
    data['status'] = 1
    json_data = json.dumps(data)
    json_object = json.loads(json_data)
    return json.dumps(json_object, indent=1)


if __name__ == "__main__":
    app.run(debug=True)
# -*- coding: utf-8 -*-

