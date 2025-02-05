import csv

region_sales = {}
product_sales = {}
salesperson_sales = {}

with open("input.csv", "r") as f:
    data = csv.DictReader(f)

    sales_volume = 0
    for line in data:
        region = line["Region"]
        salesperson = line["Salesperson"]
        product = line["Product"]
        sales = int(line["Sales"])
        units = int(line["Units"])

        #print(line)
        #sales_volume += int(line["Sales"])

        if region not in region_sales:
            region_sales[region] = {"sales_volume": 0, "total_units": 0}

        if product not in product_sales:
            product_sales[product] = {"sales_volume": 0, "total_units": 0}

        if salesperson not in salesperson_sales:
            salesperson_sales[salesperson] = {"sales_volume": 0, "total_units": 0}

        region_sales[region]["sales_volume"] += sales
        region_sales[region]["total_units"] += units

        product_sales[product]["sales_volume"] += sales
        product_sales[product]["total_units"] += units

        salesperson_sales[salesperson]["sales_volume"] += sales
        salesperson_sales[salesperson]["total_units"] += units




#print(sales_volume)
# print(region_sales)
# print(product_sales)
# print(salesperson_sales)

with open("reports/region_sales.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Region", "Sales Volume", "Units Sold"])
    for region, data in region_sales.items():
        writer.writerow([region, data["sales_volume"], data["total_units"]])

with open("reports/product_sales.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Sales Volume", "Units Sold"])
    for region, data in product_sales.items():
        writer.writerow([region, data["sales_volume"], data["total_units"]])

with open("reports/person_sales.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Salesperson", "Sales Volume", "Units Sold"])
    for region, data in salesperson_sales.items():
        writer.writerow([region, data["sales_volume"], data["total_units"]])