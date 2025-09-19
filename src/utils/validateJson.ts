

export const validationJson = (jsonStringValue: string) => {
  const jsonString = JSON.stringify(jsonStringValue);
   try {
    if (JSON.parse(jsonString)) {
      console.log('valid json');
    }
   } catch (error) {
    console.error(`Ошибка в валидации JSON: ${jsonStringValue}`);
   }
}