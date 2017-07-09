#ifndef KEECRYPTWINDOW_H
#define KEECRYPTWINDOW_H

#include <QMainWindow>

namespace Ui {
class KeecryptWindow;
}

class KeecryptWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit KeecryptWindow(QWidget *parent = 0);
    ~KeecryptWindow();

private:
    Ui::KeecryptWindow *ui;
};

#endif // KEECRYPTWINDOW_H
