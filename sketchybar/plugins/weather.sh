#!/bin/zsh

declare -A WEATHER_ICONS=(
  ["clear"]="􀆬"
  ["partly cloudy"]="􀇕"
  ["cloudy"]="􀇃"
  ["overcast"]="􀇕"
  ["fog"]="􀇊"
  ["rain"]="􀇇"
  ["drizzle"]="􀇍"
  ["snow"]="􀇏"
  ["thunderstorm"]="􀇟"
  ["freezing rain"]="􀇑"
)

# Poznan coordinates
LAT=52.4064
LON=16.9252

WEATHER_JSON=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=$LAT&longitude=$LON&current=temperature_2m,weather_code&timezone=auto")

if [ -z "$WEATHER_JSON" ]; then
  sketchybar --set $NAME label="Poznan"
  return
fi

TEMPERATURE=$(echo "$WEATHER_JSON" | jq '.current.temperature_2m')
TEMPERATURE_ROUNDED=$(printf "%.0f" "$TEMPERATURE")
WEATHER_CODE=$(echo "$WEATHER_JSON" | jq '.current.weather_code')

case "$WEATHER_CODE" in
  0) DESC="clear" ;;
  1|2) DESC="partly cloudy" ;;
  3) DESC="overcast" ;;
  45|48) DESC="fog" ;;
  51|53|55) DESC="drizzle" ;;
  61|63|65|80|81|82) DESC="rain" ;;
  71|73|75|77|85|86) DESC="snow" ;;
  95|96|99) DESC="thunderstorm" ;;
  *) DESC="unknown" ;;
esac

ICON="${WEATHER_ICONS[$DESC]}"
[ -z "$ICON" ] && ICON="􀅍"

sketchybar --set $NAME \
  icon="$ICON" \
  label="${TEMPERATURE_ROUNDED}°C"
