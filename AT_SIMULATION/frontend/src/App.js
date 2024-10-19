import { createBrowserRouter, RouterProvider, Route, createRoutesFromElements } from "react-router-dom";
import { Empty, Result } from "antd";

import Layout from "./components/Layout";
import NotFound from "./components/NotFound";
import Model from "./components/models/Model";
import Token from "./components/Token";

export const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path="" element={<Layout />} errorElement={<NotFound />}>
            <Route path="/token" element={<Token />} />
            <Route path="/not-authorized" element={<Result status="error" title="Вы не авторизованы" />} />
            <Route
                path=""
                element={
                    <Empty style={{ position: "relative", top: "50%", transform: "translate(0%, -50%)" }} description="Выберите файл имитационной модели для редактирования" />
                }
            />
            <Route
                path="/models"
                element={
                    <Empty style={{ position: "relative", top: "50%", transform: "translate(0%, -50%)" }} description="Выберите файл имитационной модели для редактирования" />
                }
            />
            <Route
                path="/models/new"
                element={
                    <Empty style={{ position: "relative", top: "50%", transform: "translate(0%, -50%)" }} description="Выберите файл имитационной модели для редактирования" />
                }
            />
            <Route path="/models/:modelId" element={<Model />}>
                <Route path="" element={<>Предполагается граф</>} />
                <Route path="resource-types">
                    <Route path="" element={<>Предполагается граф с выделенными узлами-типами ресурсов</>} />
                    <Route path="new" element={<>Предполагается модальное окно с созданием типа ресурса</>} />
                    <Route path=":resourceTypeId">
                        <Route path="" element={<>Предполагается граф с выделенным узлом-типом ресурса</>} />
                        <Route path="edit" element={<>Предполагается модальное окно с редактированием типа ресурса</>} />
                    </Route>
                </Route>
                <Route path="resources">
                    <Route path="" element={<>Предполагается граф с выделенными узлами-ресурсами</>} />
                    <Route path="new" element={<>Предполагается модальное окно с созданием ресурса</>} />
                    <Route path=":resourceId">
                        <Route path="" element={<>Предполагается граф с выделенным узлом-ресурсом</>} />
                        <Route path="edit" element={<>Предполагается модальное окно с редактированием ресурса</>} />
                    </Route>
                </Route>
                <Route path="templates">
                    <Route path="" element={<>Предполагается граф с выделенными узлами-образцами операций</>} />
                    <Route path="new" element={<>Предполагается модальное окно с созданием образца операции</>} />
                    <Route path=":templateId">
                        <Route path="" element={<>Предполагается граф с выделенным узлом-образцом операции</>} />
                        <Route path="edit" element={<>Предполагается модальное окно с редактированием образца операции</>} />
                    </Route>
                </Route>
                <Route path="template-usages">
                    <Route path="" element={<>Предполагается граф с выделенными узлами-операциями</>} />
                    <Route path="new" element={<>Предполагается модальное окно с созданием операции</>} />
                    <Route path=":templateUsageId">
                        <Route path="" element={<>Предполагается граф с выделенным узлом-операцией</>} />
                        <Route path="edit" element={<>Предполагается модальное окно с редактированием операции</>} />
                    </Route>
                </Route>
                <Route path="funcs">
                    <Route path="" element={<>Предполагается граф с выделенными узлами-функциями</>} />
                    <Route path="new" element={<>Предполагается модальное окно с созданием функции</>} />
                    <Route path=":funcId">
                        <Route path="" element={<>Предполагается граф с выделенным узлом-функцией</>} />
                        <Route path="edit" element={<>Предполагается модальное окно с редактированием функции</>} />
                    </Route>
                </Route>
            </Route>
        </Route>
    )
);

export default () => <RouterProvider router={router} />;
