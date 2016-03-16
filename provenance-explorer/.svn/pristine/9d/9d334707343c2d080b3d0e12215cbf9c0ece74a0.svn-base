<%@ taglib uri="http://java.sun.com/portlet_2_0" prefix="portlet" %>
<%@ taglib uri="http://liferay.com/tld/portlet" prefix="liferay-portlet" %>

<%@ page import="com.liferay.portal.kernel.portlet.LiferayWindowState"%>
<%@ page import="com.liferay.portal.theme.ThemeDisplay"%>

<portlet:defineObjects />

<%ThemeDisplay themeDisplay = (ThemeDisplay)request.getAttribute("THEME_DISPLAY");%>

<liferay-portlet:renderURL windowState="<%= LiferayWindowState.EXCLUSIVE.toString()%>" var="iframeURL_tutorial">
	<portlet:param name="jspPage" value="/html/mapgui_tutorial.jsp"/>
</liferay-portlet:renderURL> 

<liferay-portlet:renderURL windowState="<%= LiferayWindowState.EXCLUSIVE.toString()%>" var="iframeURL">
	<portlet:param name="jspPage" value="/html/mapgui.jsp"/>
</liferay-portlet:renderURL> 

