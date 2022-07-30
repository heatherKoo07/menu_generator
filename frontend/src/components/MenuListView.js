import axios from "axios";
import { Card, Tag, Space } from "antd";
import React, { useEffect, useState } from "react";
import MenuAddForm from "./MenuAddForm";

const MenuListView = () => {
  const [menuList, setMenuList] = useState([]);
  const [updated, setUpdated] = useState(true);

  useEffect(() => {
    if (updated) {
      axios
        .get("/menu")
        .then(function (response) {
          setMenuList(response.data.menus);
        })
        .catch(function (error) {
          console.log(error);
        });
      setUpdated(false);
    }
  }, [updated, setUpdated]);

  const onClose = (element) => {
    axios
      .delete("/menu", {
        data: {
          menu: element,
        },
      })
      .then(function (response) {
        console.log(response);
        setUpdated(true);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <>
      <Card title={`You have a total of ${menuList.length} menu(s)`}>
        <MenuAddForm setUpdated={setUpdated} />
        {menuList.map((element) => (
          <Tag key={element} closable onClose={() => onClose(element)}>
            {element}
          </Tag>
        ))}
      </Card>
    </>
  );
};

export default MenuListView;
