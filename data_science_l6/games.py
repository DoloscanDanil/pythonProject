print(data.isnull().sum())

data = data.dropna()



game = data.groupby("Genry")["Global_Sales"].count().head(10)
custom_colors = mpl.colors.Normalize(vmin=min(game), vmax=max(game))
colours = [mpl.cm.PuBu(custom_colors(i))for i in game]
plt.figure(figsize=(7, 7))

x = data[["Rank", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]]

y = data["Global_Sales"]

xtrain, xtest, ytrain, ytest = train_test_split(x, y test_size=0.2,random_state=42)

model = LinearRegission
model
