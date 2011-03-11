# Reads csv data created by analyze.py and makes graphs

# Read csv data
# t <- read.csv(file="out.csv")

# Plot density info
# png('graphs/density.png', width=1600)
# plot(t,ylab='score', xlab='datetime')
# dev.off()

t <- read.csv(file="csv/combine.csv")

# Write to png
png('graphs/densities.png', width=1600, height=960)
par(mfrow=c(2,1))
plot(t$date, t$total, ylab="Number of Tweets", xlab="Datetime (utc)", main="Total Number of Tweets Received")
plot(t$date, t$english, ylab="% English", xlab="Datetime (utc)", main="% Tweets English")
dev.off()
