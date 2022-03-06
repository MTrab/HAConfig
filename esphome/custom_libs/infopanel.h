/* Map days */
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