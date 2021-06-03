#include <iostream>
#include <string>
#include <vector>
#include <sqlite3.h>
#include <gtkmm.h>

#include "mywin.h"

/*
pkg-config
sqlit3
gtkmm-3.0

g++  `pkg-config --cflags --libs gtkmm-3.0` main.cc  -lsqlite3
*/
int Callback(void*_Pointer, int argc, char **argv, char **columnNames)
{
    std::vector<std::string> * Pointer = (std::vector<std::string> *)_Pointer;
    for(int i=1; i<argc; i++)
    {    
        Pointer->push_back(columnNames[i]);
    }
    return 0;
}

int main(int argc, char *argv[])
{
    char  *err = nullptr;
    if(argc==1)
    {
        return -1;
    }  
    sqlite3 * con = nullptr;
    int ok = sqlite3_open(argv[1], &con);
    //argc--;
    //argv--;
    if(ok != SQLITE_OK)
    {
        return -2;
    }

    //hole spalten namen
    std::vector<std::string> columns;
    ok = sqlite3_exec(con, 
        "SELECT * from alben LIMIT 1",
        Callback,
        &columns,
        &err);
    if(ok != SQLITE_OK)
    {
        std::cout << err << std::endl;
        sqlite3_free(err);
        return -3;
    }

    for(auto x:columns)
        std::cout << x << std::endl;

    //auto app = Gtk::Application::create(argc, argv, "org.gtkmm.examples.base");

    Gtk::Main app(argc, argv);
    mywin win(columns, con);


    win.show_all();

    app.run(win);

    sqlite3_close(con);
}
