#include <iostream>
#include <string>
#include <vector>
#include <sqlite3.h>
#include <gtkmm.h>

#include "mywin.h"
#include "dbsqlite3.h"


int main(int argc, char *argv[])
{

    if(argc<3)
        return -1;

    dbsqlite3 con(argv[1]);

    std::vector<std::string> columns = con.getColumnNames(argv[2]);

    Gtk::Main app(argc, argv);

    mywin win(columns, &con, argv[2]);

    win.show_all();

    app.run(win);
}
