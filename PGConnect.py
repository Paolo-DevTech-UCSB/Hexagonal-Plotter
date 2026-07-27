# -*- coding: utf-8 -*-
import asyncio
import asyncpg

async def Get_PG_Info_By_Name(proto_name_list, stage, sort=None):
    if not proto_name_list:
        return None

    conn = await asyncpg.connect(
        database="hgcdb",
        host="gut.physics.ucsb.edu",
        user="postgres",
        password="hepuser",
        port="5432"
    )

    placeholder_list = ','.join(f'${i}' for i in range(1, len(proto_name_list) + 1))

    # Choose table + key
    if stage == 'module':
        table = "module_inspect"
        key_name = "module_name"
    elif stage == 'protomodule':
        table = "proto_inspect"
        key_name = "proto_name"
    else:
        await conn.close()
        raise ValueError("Invalid stage")

    # Base query
    query = (
        f"""
        SELECT {key_name}, x_points, y_points, z_points,
               date_inspect, time_inspect
        FROM {table}
        WHERE {key_name} IN ({placeholder_list})
        """
    )

    # Add sorting if requested
    if sort == "newest":
        query += " ORDER BY date_inspect DESC, time_inspect DESC LIMIT 1"
    elif sort == "oldest":
        query += " ORDER BY date_inspect ASC, time_inspect ASC LIMIT 1"

    rows = await conn.fetch(query, *proto_name_list)
    await conn.close()

    if not rows:
        return None

    # Return ONLY ONE entry
    row = rows[0]

    return {
        key_name: row[key_name],
        "x_points": row["x_points"],
        "y_points": row["y_points"],
        "z_points": row["z_points"],
        "date_inspect": row["date_inspect"],
        "time_inspect": row["time_inspect"]
    }

def convert_pg_to_ogp_format(pg_row):
    module_name = pg_row["module_name"]
    x_points = pg_row["x_points"]
    y_points = pg_row["y_points"]
    z_points = pg_row["z_points"]

    # Build the Selected File path

    # Build Heightlist2
    heightlist2 = []
    heightlist2.append(['#', 'X', 'Z', '#'])

    for i in range(len(x_points)):
        flatname = f"flatness{i+1}"

        heightlist2.append([flatname, 'X', str(x_points[i]), flatname])
        heightlist2.append(['', 'Y', str(y_points[i]), ''])
        heightlist2.append(['', 'Z', str(z_points[i]), ''])

    return {
        "Heightlist2": heightlist2,
        "Length": len(heightlist2)
    }


def main(modulename, sort="newest"):
    row = asyncio.run(Get_PG_Info_By_Name([modulename], 'module', sort=sort))
    ogp_data = convert_pg_to_ogp_format(row)

    print("Length:", ogp_data["Length"])

    for line in ogp_data["Heightlist2"]:
        print(line)

    return ogp_data


#if __name__ == "__main__":
    # Example usage
#    print(main("320MHF2TDSB0238", sort="newest"))


###  make diff needs this:    selected_file, selected_file2, folder_path, modulename, modulename2, ShapeID, ShapePlot, FileName



#EXAMPLE OUTPUT
r"""PS C:\Users\Admin\Documents\GitHub\HexPlots\Hexagonal-Plotter> & C:/Users/Admin/AppData/Local/Programs/Python/Python313/python.exe c:/Users/Admin/Documents/GitHub/HexPlots/Hexagonal-Plotter/PGConnect.py
Length: 73
['#', 'X', 'Z', '#']
['flatness1', 'X', '170.16091918945312', 'flatness1']
['', 'Y', '146.07310485839844', '']
['', 'Z', '2.967017412185669', '']
['flatness2', 'X', '171.4767303466797', 'flatness2']
['', 'Y', '111.91995239257812', '']
['', 'Z', '2.985647201538086', '']
['flatness3', 'X', '170.7286376953125', 'flatness3']
['', 'Y', '71.90270233154297', '']
['', 'Z', '3.033262014389038', '']
['flatness4', 'X', '155.6975555419922', 'flatness4']
['', 'Y', '51.84480285644531', '']
['', 'Z', '2.989896297454834', '']
['flatness5', 'X', '134.00265502929688', 'flatness5']
['', 'Y', '38.30419921875', '']
['', 'Z', '2.9582839012145996', '']
['flatness6', 'X', '102.82559204101562', 'flatness6']
['', 'Y', '20.028644561767578', '']
['', 'Z', '2.9336462020874023', '']
['flatness7', 'X', '79.95062255859375', 'flatness7']
['', 'Y', '19.969451904296875', '']
['', 'Z', '2.974250078201294', '']
['flatness8', 'X', '47.53782653808594', 'flatness8']
['', 'Y', '40.114967346191406', '']
['', 'Z', '3.0016162395477295', '']
['flatness9', 'X', '21.718111038208008', 'flatness9']
['', 'Y', '55.23408889770508', '']
['', 'Z', '3.011315107345581', '']
['flatness10', 'X', '9.313248634338379', 'flatness10']
['', 'Y', '70.69165802001953', '']
['', 'Z', '2.9869577884674072', '']
['flatness11', 'X', '9.334585189819336', 'flatness11']
['', 'Y', '102.26820373535156', '']
['', 'Z', '3.155447483062744', '']
['flatness12', 'X', '9.358421325683594', 'flatness12']
['', 'Y', '140.34373474121094', '']
['', 'Z', '3.157670736312866', '']
['flatness13', 'X', '27.662355422973633', 'flatness13']
['', 'Y', '166.48660278320312', '']
['', 'Z', '3.069383144378662', '']
['flatness14', 'X', '52.31438064575195', 'flatness14']
['', 'Y', '176.8903350830078', '']
['', 'Z', '3.035184621810913', '']
['flatness15', 'X', '108.3060073852539', 'flatness15']
['', 'Y', '191.39768981933594', '']
['', 'Z', '3.001317024230957', '']
['flatness16', 'X', '136.65841674804688', 'flatness16']
['', 'Y', '173.57261657714844', '']
['', 'Z', '2.971609115600586', '']
['flatness17', 'X', '160.1805419921875', 'flatness17']
['', 'Y', '161.67193603515625', '']
['', 'Z', '2.9667515754699707', '']
['flatness18', 'X', '139.78082275390625', 'flatness18']
['', 'Y', '141.19219970703125', '']
['', 'Z', '2.9666335582733154', '']
['flatness19', 'X', '145.6484375', 'flatness19']
['', 'Y', '75.08819580078125', '']
['', 'Z', '2.977083444595337', '']
['flatness20', 'X', '88.462890625', 'flatness20']
['', 'Y', '63.64320755004883', '']
['', 'Z', '3.0228779315948486', '']
['flatness21', 'X', '54.937286376953125', 'flatness21']
['', 'Y', '87.33502197265625', '']
['', 'Z', '3.0476467609405518', '']
['flatness22', 'X', '53.8161506652832', 'flatness22']
['', 'Y', '144.7476348876953', '']
['', 'Z', '3.0362942218780518', '']
['flatness23', 'X', '89.74131774902344', 'flatness23']
['', 'Y', '178.58738708496094', '']
['', 'Z', '2.99800443649292', '']
['flatness24', 'X', '105.76856231689453', 'flatness24']
['', 'Y', '111.69657135009766', '']
['', 'Z', '3.02891206741333', '']"""