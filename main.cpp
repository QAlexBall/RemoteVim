//
// Created by deren zhu on 2019/11/17.
//

#include <iostream>
#include <spdlog/spdlog.h>
#include "src/Host.h"
#include "src/Session.h"

int main() {
    Host host("chris", "119.23.33.220", 22);
    Session session(host);
    std::cout << host.get_username() << std::endl;
    session.set_current_path("/home/chris");
    auto out = session.get_output("ls");
    for (auto & it : out) {
        spdlog::info("item begin =>{}<= end", it);
    }
}

