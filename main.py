import time
from time import sleep
from cffi.cffi_opcode import CLASS_NAME
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    car_comfort_icon= (By.XPATH, "//div[@class='tcard-title' and text()= 'Comfort']")

    #Localizadores de prueba dos para campo Phone y Code
    number_field = (By.CLASS_NAME, "np-button")
    number_second_file = (By.ID, 'phone')
    button_next = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    code_field = (By.XPATH, '//input[@id="code"]')
    button_confirm = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Confirmar')]")

    #Localizar campo metodo pago
    payment_method = (By.CSS_SELECTOR, '.pp-text')
    add_card = (By.CSS_SELECTOR, ".pp-row.disabled") #field agregar tarjeta
    card_number_field = (By.XPATH, "//input[@class='card-input' and @name='number']" )
    card_code_cvv = (By.XPATH, "//div[@class='card-code-input']/input[@id='code']")
    button_pay_add = (By.XPATH, "//button[contains(text(), 'Agregar')]")
    colors_space = (By.CLASS_NAME, 'plc')

    #Localizadores mensaje a conductor
    close_button_payment = (By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/button')
    message_field = (By.XPATH, '/html/body/div[1]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div')
    message_2 =(By.ID, "comment")

    #Localizadores manta y Helados
    sliding_button = (By.CSS_SELECTOR, ".switch .slider.round")
    counter_button_ice = (By.CSS_SELECTOR, "div.counter > div.counter-plus")
    counter_button_plus = (By.CLASS_NAME, "counter-value")

    #Ultima prueba - pedir taxi
    button_order_taxi = (By.CLASS_NAME, 'smart-button-wrapper')



    def __init__(self, driver):
        self.driver = driver

    def set_from(self, address_from):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(address_from)

    def set_to(self, address_to):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self,address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_request_text_button(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.request_taxi_button))

    def click_on_request_taxi_button(self):
        self.get_request_text_button().click()

    def get_comfort_icon(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.car_comfort_icon)
        )
    def click_on_comfort_icon(self):
        self.get_comfort_icon().click()



#Metodos prueba 3
    def get_number_field(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.number_field)
        )

    def click_on_number_field(self):
        self.get_number_field().click()

    def get_number_(self):
        return self.driver.find_element(*self.number_second_file).text

    def get_number_second_filed(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.number_second_file)
        )

    def set_on_second_number_field(self, phone_number ):
           WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.number_second_file)
            ).send_keys(phone_number)

    def click_on_second_number_field(self): #click al segundo campo para numero
        self.set_on_second_number_field(data.phone_number)

    def get_on_next_button(self):
        return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.button_next))

    def click_on_next_button(self):
        return self.get_on_next_button().click() #LISTO HASTA ACA

    #Metodo get para llamar campo del cod , configurarlo con el retrive
    def get_on_code_number(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.code_field)
        )

    def set_on_code_number(self):
        code = retrieve_phone_code(driver=self.driver)  # Llamar a la función externa
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.code_field)
        ).send_keys(code)

    def get_confirm_button(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_confirm)
        )

    def click_on_confirm_button(self):
        return self.get_confirm_button().click()

#Metodos para pruebas numero 4
    def get_payment_method(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method)
        )

    def click_on_payment_method(self):
        return self.get_payment_method().click() # clic al primer boton

    def  get_add_card_method(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card)
        )
    def click_on_add_card(self):
        return self.get_add_card_method().click() # clic al segundo boton - HASTA AQUI BIEN !


    def get_card_number_field(self): #llamar el campo de numero de tc
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_number_field)
        )

    def set_card_number_field(self):
        self.get_card_number_field().send_keys(data.card_number)

    def get_card_code_cvv(self):  # llamar el campo de numero de tc
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_code_cvv))

    def set_code_cvv_field(self):
        self.get_card_code_cvv().send_keys(data.card_code)

    def get_color_space(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.colors_space)
        )

    def click_color_space(self):
        return self.get_color_space().click()  # clic al segundo boton


    def get_button_add_card(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_pay_add)
        )

    def click_on_button_add_card(self):
        return self.get_button_add_card().click()  # clic boton agregar

#Metodos prueba 5
    def get_close_button_payment(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.close_button_payment)
        )
    def click_on_close_button_payment(self):
        return self.get_close_button_payment().click()  #HASTA AQUI PERFECTO


    def get_message_to_taxi_field_clic(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.message_field)
        )
    def click_on_message_to_taxi_driver(self):
        return self.get_message_to_taxi_field_clic().click()



    def get_message_to_taxi_driver(self):
        return self.driver.find_element(*self.message_2)

    def set_message_to_taxi_driver(self):
        message_field = self.get_message_to_taxi_driver()
        message_field.clear()
        message_field.send_keys(data.message_for_driver)

#metodos PRUEBA 6

    def set_button_slider(self):
        button_slider_field = self.driver.find_element(*self.sliding_button)
        button_slider_field.click()
#Metodo prueba 7

    def set_counter_button_ice_field(self):
        button_ice = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.counter_button_ice))
        button_ice.click()
        button_ice.click()

#Metodo prueba 8
    def set_button_order_taxi(self):
        button_order_taxi_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_order_taxi)
        )
        button_order_taxi_field.click()





class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(service=Service(), options=options)

    def test1_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test2_select_comfort(self):
        #self.test1_set_route() # traer cod del test anterior
        routes_page = UrbanRoutesPage(self.driver) #crear objeto pag.
        routes_page.click_on_request_taxi_button() #metodo clic de la clase anterior del elemento de la pag
        routes_page.click_on_comfort_icon()
        assert routes_page.get_comfort_icon().text == "Comfort"


    def test3_select_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_number_field()
        routes_page.click_on_second_number_field()
        assert data.phone_number == routes_page.get_number_second_filed().get_property('value')
        routes_page.click_on_next_button()
        routes_page.set_on_code_number()
        routes_page.click_on_confirm_button()

    def test4_add_payment_method(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_payment_method()
        routes_page.click_on_add_card()
        routes_page.set_card_number_field()
        routes_page.set_code_cvv_field()
        routes_page.click_color_space()
        routes_page.click_on_button_add_card()
        assert data.card_code == routes_page.get_card_code_cvv().get_property('value')
        assert data.card_number == routes_page.get_card_number_field().get_property('value')

    def test5_write_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_close_button_payment()
        routes_page.click_on_message_to_taxi_driver()
        routes_page.set_message_to_taxi_driver()
        assert data.message_for_driver == routes_page.get_message_to_taxi_driver().get_attribute('value')


    def test6_click_sliding_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_button_slider()
        assert self.driver.find_element(*routes_page.sliding_button).is_displayed()

    def test7_ice_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_counter_button_ice_field()
        assert self.driver.find_element(*routes_page.counter_button_plus).text == "2"

    def test8_button_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_button_order_taxi()
        assert self.driver.find_element(*routes_page.button_order_taxi).is_displayed()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


