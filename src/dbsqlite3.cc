#include <gtkmm.h>
#include "dbsqlite3.h"

//konstuktor
dbsqlite3::dbsqlite3(const std::string &fn)
{  
  int ok = sqlite3_open(fn.c_str(), &con);
  if(ok != SQLITE_OK)
    {
      throw fn + " kann nicht geöffnet werde";
    }
}

//destruktor
dbsqlite3::~dbsqlite3()
{
    sqlite3_close(con);
    con = nullptr;
}

//Callback um Spaltennamen zu finde
int CallbackSpalten(void*_Pointer, int argc, char **argv, char **columnNames)
{
    std::vector<std::string> * Pointer = (std::vector<std::string> *)_Pointer;
    for(int i=0; i<argc; i++)
    {    
        Pointer->push_back(columnNames[i]);
    }
    return 0;
}

//finde spaltennamen
std::vector<std::string> dbsqlite3::getColumnNames(const std::string &tname)
{    
    char  *err = nullptr;
    std::vector<std::string> columns;
    std::string query = "SELECT * from " + tname + " LIMIT 1";

    int ok = sqlite3_exec(con, 
        query.c_str(),
        CallbackSpalten,
        &columns,
        &err);
    
    if(ok != SQLITE_OK)
    {
        std::cout << err << std::endl;
        sqlite3_free(err);
    }
    return columns;
}


/*
  wird fuer jede Zeil aufgerufen
  erweitert ListStore und fiellt neue Zeile
*/
int CallbackQuery(void *_Pointer, int argc, char **argv, char **columnNames)
{
  Gtk::ListStore *content = (Gtk::ListStore *) _Pointer;
  auto row = *(content->append());
  
  for(int i=0; i<argc; i++)
    {    
      gtk_list_store_set(content->gobj(), row.gobj(), i-1, argv[i], -1); 
    }
  return 0;
  
}

//führe query aus und füll in Liststor
void dbsqlite3::query_fill_liststore(const std::string &query,
                Gtk::ListStore *content){
 char  *err = nullptr;
 int ok = sqlite3_exec(con, 
		       query.c_str(),
		       CallbackQuery,
		       content,
		       &err);
 if(ok != SQLITE_OK)
   {
     std::cout << err << std::endl;
     sqlite3_free(err);
   }
}

