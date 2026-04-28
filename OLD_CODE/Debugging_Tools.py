def measurement_matrix(measurements):
    table = []
    for mtype, entries in measurements.items():
        for suffix, info in entries:
            # Try to extract cycle number from filename
            cycle = None
            for word in suffix.replace(".xls", "").split():
                if word.isdigit():
                    cycle = word
            if cycle is None:
                cycle = suffix  # fallback if no cycle number

            table.append([
                cycle,
                info["flatness"],
                info["z_average"],
                info["z_max"],
                info["range"], 
                mtype
            ])

        # Print nicely formatted table
    #print(table)
    return table
