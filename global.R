library(shiny)
library(maps)
library(mapdata)
library(maptools)
library(stringi)


# setwd("C:/Users/bliap/Documents/R/Weather_Data_Explorer")

weather <- read.csv("data/weather.csv")
weather$time <- as.POSIXlt(weather$time, format = "%Y-%m-%d %H:%M:%S", tz = "UTC")

## preprocessing with map data

map = readShapePoly('data/bou2_4p.shp')


## add chinese font

font_home <- function(path = '') file.path('~', '.fonts', path)
if (Sys.info()[['sysname']] == 'Linux' &&
        system('locate wqy-zenhei.ttc') != 0 &&
        !file.exists(font_home('wqy-zenhei.ttc'))) {
    if (!file.exists('wqy-zenhei.ttc'))
        shiny:::download(
            'https://github.com/rstudio/shiny-examples/releases/download/v0.10.1/wqy-zenhei.ttc',
            'wqy-zenhei.ttc'
        )
    dir.create(font_home())
    file.copy('wqy-zenhei.ttc', font_home())
    system2('fc-cache', paste('-f', font_home()))
}
rm(font_home)