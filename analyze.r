# Reads csv data created by analyze.py and makes graphs

# Read csv data
t <- read.csv(file="out.csv")

# Plot density info
png('graphs/density.png', width=1600)
plot(t,ylab='score', xlab='datetime')
dev.off()
