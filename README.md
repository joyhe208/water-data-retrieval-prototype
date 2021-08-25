Prototype for Hydrodetectus automated water-data retrieval system
------------------------------------------------------------------

Bare-bones web app that provides a downloadable file and matrix/linechart visualizations of streamflow/climatic data at various stations in California. The website also shows geographical data of stations, constractors, urban areas, power plants, etc. The user retrieves data visually, by dragging their mouse across an area on the map, which sends a post request to the server. The Flask app then calls constructors in the GetData module, which makes use of the SQLTranslate package (https://github.com/joyhe208/pkg_sqltranslate) to retrieve database streamflow and climatic data of all stations within the area selected.

