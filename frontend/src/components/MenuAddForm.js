import axios from "axios";
import { Button, Form, Input, Typography } from "antd";
import React from "react";
const { Text } = Typography;

const MenuAddForm = ({ setUpdated }) => {
  const [form] = Form.useForm();
  const onFinish = (values) => {
    console.log("Received values from form: ", values);
    // post request
    axios
      .post("/menu", {
        menu: values.menu,
      })
      .then(function (response) {
        console.log(response);
        setUpdated(true);
      })
      .catch(function (error) {
        console.log(error);
      });
    form.resetFields();
  };
  // TODO add validation
  return (
    <Form
      layout="inline"
      form={form}
      onFinish={onFinish}
      style={{ marginBottom: "25px" }}
    >
      <Form.Item name="menu" noStyle>
        <Input
          style={{
            width: "calc(100% - 200px)",
          }}
          placeholder="Add Menu"
          autoFocus
        />
        {/* <Input.Group compact>
          <Input
            style={{
              width: "calc(100% - 200px)",
            }}
            placeholder="Add Menu"
          />
          <Button type="primary" htmlType="submit">
            Add
          </Button>
        </Input.Group> */}
      </Form.Item>

      <Form.Item noStyle>
        <Button type="primary" htmlType="submit">
          Add
        </Button>
      </Form.Item>
    </Form>
  );
};

export default MenuAddForm;
