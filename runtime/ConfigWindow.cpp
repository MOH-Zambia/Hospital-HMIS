//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// ConfigWindow.h - Configuration window
//
//////////////////////////////////////////////////////////////////////////

#include "ConfigWindow.h"
#include "ui_ConfigWindow.h"

ConfigWindow::ConfigWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ConfigWindow)
{
    ui->setupUi(this);
}

ConfigWindow::~ConfigWindow()
{
    delete ui;
}

void ConfigWindow::on_buttonBox_accepted()
{
    this->close();
}

void ConfigWindow::on_buttonBox_rejected()
{
    this->close();
}

void ConfigWindow::on_chkFixedPort_stateChanged(int state)
{
    if (state == Qt::Checked)
        ui->spinPortNumber->setEnabled(true);
    else
        ui->spinPortNumber->setEnabled(false);
}

QString ConfigWindow::getBrowserCommand()
{
    return ui->browserCommandLineEdit->text();
}

bool ConfigWindow::getFixedPort()
{
    return ui->chkFixedPort->isChecked();
}

int ConfigWindow::getPortNumber()
{
    return ui->spinPortNumber->value();
}

bool ConfigWindow::getOpenTabAtStartup()
{
    return ui->chkOpenTabAtStartup->isChecked();
}

QString ConfigWindow::getPythonPath()
{
    return ui->pythonPathLineEdit->text();
}

QString ConfigWindow::getApplicationPath()
{
    return ui->applicationPathLineEdit->text();
}


void ConfigWindow::setBrowserCommand(QString command)
{
    ui->browserCommandLineEdit->setText(command);
}

void ConfigWindow::setFixedPort(bool fixedPort)
{
    if (fixedPort)
    {
        ui->chkFixedPort->setCheckState(Qt::Checked);
        ui->spinPortNumber->setEnabled(true);
    }
    else
    {
        ui->chkFixedPort->setCheckState(Qt::Unchecked);
        ui->spinPortNumber->setEnabled(false);
    }
}

void ConfigWindow::setPortNumber(int port)
{
    ui->spinPortNumber->setValue(port);
}

void ConfigWindow::setOpenTabAtStartup(bool openTabAtStartup)
{
    if (openTabAtStartup)
    {
        ui->chkOpenTabAtStartup->setCheckState(Qt::Checked);
    }
    else
    {
        ui->chkOpenTabAtStartup->setCheckState(Qt::Unchecked);
    }
}

void ConfigWindow::setPythonPath(QString path)
{
    ui->pythonPathLineEdit->setText(path);
}

void ConfigWindow::setApplicationPath(QString path)
{
    ui->applicationPathLineEdit->setText(path);
}

