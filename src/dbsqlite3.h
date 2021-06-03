#ifndef _MYDB_
#define _MYDB_

#include <string>
#include <vector>
#include <iostream>
#include <sqlite3.h>

namespace{
    class ListStore;
}
class dbsqlite3
{
private:
    sqlite3 * con = nullptr;

public:
    dbsqlite3(const std::string &fname);

    ~dbsqlite3();

    std::vector<std::string> getColumnNames(const std::string &tname);

    void query_fill_liststore(const std::string &query,
                Gtk::ListStore *content);
};




#endif