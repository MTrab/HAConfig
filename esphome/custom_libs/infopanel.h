/* Map days */
std::map<std::string, std::string> dayMapWeather {
    {"0", "Man"},
    {"1", "Tir"},
    {"2", "Ons"},
    {"3", "Tor"},
    {"4", "Fre"},
    {"5", "Lør"},
    {"6", "Søn"}
};

std::map<int, std::string> dayMapInt {
    {1, "Man"},
    {2, "Tir"},
    {3, "Ons"},
    {4, "Tor"},
    {5, "Fre"},
    {6, "Lør"},
    {7, "Søn"}
};

/* Map months */
std::map<std::string, std::string> monthMap {
    {"01", "Jan"},
    {"02", "Feb"},
    {"03", "Mar"},
    {"04", "Apr"},
    {"05", "Maj"},
    {"06", "Jun"},
    {"07", "Jul"},
    {"08", "Aug"},
    {"09", "Sep"},
    {"10", "Okt"},
    {"11", "Nov"},
    {"12", "Dec"}
};

/* Map weathericons */
std::map<std::string, std::string> conditionMap {
    {"sunny", "\U000F0599"},
    {"partlycloudy", "\U000F0595"},
    {"cloudy", "\U000F0590"},
    {"clear-night", "\U000F0594"},
    {"rainy", "\U000F0597"},
    {"fog", "\U000F0591"},
    {"hail", "\U000F0592"},
    {"lightning", "\U000F0593"},
    {"lightning-rainy", "\U000F067E"},
    {"pouring", "\U000F0596"},
    {"snowy-rainy", "\U000F067F"},
    {"windy", "\U000F059D"},
    {"windy-variant", "\U000F059E"}
};

std::string ExtractDateTime(std::string data, int index, char delim = ';') {
    std::size_t _current, _previous = 0;
    _current = data.find(delim);

    for (int i = 0; i < index; i++) {
        _previous = _current + 1;
        _current = data.find(delim, _previous);
    }
    return data.substr(_previous, _current - _previous);
}

std::string ExtractEvent(std::string data, int index, char delim = '#') {
    std::size_t _current, _previous = 0;
    _current = data.find(delim);

    for (int i = 0; i < index; i++) {
        _previous = _current + 1;
        _current = data.find(delim, _previous);
    }
    return data.substr(_previous, _current - _previous);
}